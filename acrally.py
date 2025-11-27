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
    def __init__(self, stage, voice, call_earliness, start_button, handbrake):
        self.voice = voice
        self.call_earliness = call_earliness
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
        print(self.distance)

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

        while not self.exit_all and not self.started:
            time.sleep(0.1)

        while len(self.notes_list) > 0 and not self.exit_all:
            if self.notes_list[0]["distance"] < self.distance + (120 + (self.speed_kmh // 2)) * self.call_earliness:
                note = self.notes_list.pop(0)
                tokens = note["notes"]
                link_to_next = note["link_to_next"]
                while link_to_next:
                    next_note = self.notes_list.pop(0)
                    next_tokens = next_note["notes"]
                    tokens.extend(next_tokens)
                    link_to_next = next_note["link_to_next"]

                tokens = self.combine_tokens(tokens, token_sounds)

                for token in tokens:
                    # print(token)
                    if token in token_sounds:
                        sound = random.choice(token_sounds[token])
                        winsound.PlaySound(sound, winsound.SND_MEMORY | winsound.SND_NODEFAULT | winsound.SND_NOSTOP)
                    elif matches := re.match('Pause([\\d.]+)s(?:_Reset)?', token):
                        pause_time = float(matches.group(1))
                        print(f"Sleeping for {pause_time}")
                        time.sleep(pause_time)

            else:
                time.sleep(0.1)
        print("Speak thread closed")

    def combine_tokens(self, tokens, token_sounds):
        new_tokens = []
        i = 0
        longest_match = []
        while i + len(longest_match) < len(tokens):
            for token in tokens[i:]:
                token = str(token)
                key = longest_match + [token]
                if "-".join(key) in token_sounds:
                    longest_match = key
                else:
                    if len(longest_match) == 0:
                        longest_match.append(token)
                    new_tokens.append("-".join(longest_match))
                    i += len(longest_match)
                    longest_match = []
                    break
        if len(longest_match) > 0:
            new_tokens.append("-".join(longest_match))
        return new_tokens

    def get_distance(self):
        return self.distance

    def exit(self):
        self.exit_all = True
