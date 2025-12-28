import os.path
import random
import re
import threading
import time
from threading import Thread

import keyboard
import winsound
import yaml

from handbrake import Handbrake
from pyaccsharedmemory import accSharedMemory


class ACRally:
    def __init__(
            self,
            stage,
            voice,
            call_earliness,
            max_calls_ahead,
            call_speed_multiplier,
            start_button,
            handbrake
    ):
        self.voice = voice
        self.call_earliness = call_earliness
        self.max_calls_ahead = max_calls_ahead
        self.call_speed_multiplier = call_speed_multiplier
        self.start_button = start_button
        self.handbrake = handbrake
        self.notes_list = []
        self.exit_all = False
        self.started = False
        self.last_retrieve = time.time()
        self.speed_kmh = 0
        # Distance does not always start at 0
        self.distance = None

        self.notes_list = yaml.safe_load(open(f"pacenotes/{stage}.yml"))
        if self.notes_list is not None:
            self.distance = self.notes_list[0]["distance"]
        else:
            self.notes_list = []
            self.distance = 0

    def start(self):
        retrieve = Thread(target=self.retrieve_thread, daemon=True)
        speak = Thread(target=self.speak_thread, daemon=True)
        retrieve.start()
        speak.start()

    def retrieve_thread(self):
        asm = accSharedMemory()
        last_shared_memory = None

        handbrake_pressed = False
        if self.handbrake:
            def check_pressed_2s():
                nonlocal handbrake_pressed

                handbrake = Handbrake(self.handbrake)
                while not self.started and not self.exit_all:
                    if handbrake.get_pressed():
                        time.sleep(2)
                        if handbrake.get_pressed():
                            handbrake_pressed = True
                    time.sleep(0.1)
                handbrake.close()
            threading.Thread(target=check_pressed_2s, daemon=True).start()

        while (not keyboard.is_pressed(self.start_button) and not handbrake_pressed) and not self.exit_all:
            time.sleep(0.05)

        winsound.Beep(800, 250)

        while not self.exit_all:
            sm = asm.read_shared_memory()
            if sm is None:
                sm = last_shared_memory

            if sm is not None:
                now = time.time()
                delta_t = now - self.last_retrieve
                self.last_retrieve = now
                self.speed_kmh = sm.Physics.speed_kmh
                speed_ms = self.speed_kmh * (5/18)
                self.distance += speed_ms * delta_t

                if speed_ms > 5:
                    # Detect whether player has set off from start line
                    self.started = True

                # print(distance, sm.Static.track_length)
                last_shared_memory = sm
            else:
                # print(None)
                continue
            time.sleep(0.05)

        asm.close()
        print("Retrieve thread closed")

    def speak_thread(self):
        token_sounds = self.build_token_sounds()

        while not self.exit_all and not self.started:
            time.sleep(0.1)

        # Do not play too many notes ahead of time
        previous_distances = []

        while len(self.notes_list) > 0 and not self.exit_all:
            while len(previous_distances) > 0 and previous_distances[0] < self.distance:
                previous_distances.pop(0)

            if (len(previous_distances) < self.max_calls_ahead and self.notes_list[0]["distance"]
                    < self.distance + (80 * self.call_earliness) + ((self.speed_kmh / 9)**2 * self.call_speed_multiplier)):
                note = self.notes_list.pop(0)
                previous_distances.append(note["distance"])
                tokens = self.combine_tokens(note["notes"], token_sounds)
                link_to_next = note["link_to_next"]
                while link_to_next:
                    next_note = self.notes_list.pop(0)
                    next_tokens = self.combine_tokens(next_note["notes"], token_sounds)
                    tokens.extend(next_tokens)
                    link_to_next = next_note["link_to_next"]

                self.play_tokens(tokens, token_sounds)
            else:
                time.sleep(0.1)
        print("Speak thread closed")

    def build_token_sounds(self):
        token_sounds = {}
        for entry in os.listdir(f"voices\\{self.voice}"):
            # This regex allows for After.wav and After_1.wav, etc. and matches the main token
            matches = re.match(r"(.+?)(?:_\d+)?\.wav", entry)
            if matches:
                token = matches.group(1)
                if not token in token_sounds:
                    token_sounds[token] = []
                with open(f"voices\\{self.voice}\\{entry}", "rb") as f:
                    token_sounds[token].append(f.read())
        return token_sounds

    def combine_tokens(self, tokens, token_sounds):
        new_tokens = []
        while len(tokens) > 0:
            for i in reversed(range(len(tokens))):
                key = "-".join(tokens[:i + 1])
                # print(key)
                if key in token_sounds or i == 0:
                    # i == 0 is required for when a token does not exist
                    # e.g. PauseX.Ys
                    new_tokens.append(key)
                    tokens = tokens[i + 1:]
                    break
        return new_tokens

    def match_pause(self, token):
        if matches := re.match('Pause([\\d.]+)s(?:_Reset)?', token):
            return float(matches.group(1))
        return None

    def play_tokens(self, tokens, token_sounds):
        for token in tokens:
            # print(token)
            if token in token_sounds:
                sound = random.choice(token_sounds[token])
                winsound.PlaySound(sound, winsound.SND_MEMORY | winsound.SND_NODEFAULT | winsound.SND_NOSTOP)
            elif pause_time := self.match_pause(token):
                time.sleep(pause_time)

    def get_distance(self):
        return self.distance

    def exit(self):
        self.exit_all = True
