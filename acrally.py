import io
import os.path
import random
import re
import time
import wave
from threading import Thread

import yaml

import util
from pyaccsharedmemory import accSharedMemory


class ACRally:
    def __init__(
            self,
            stage,
            voice,
            call_earliness,
            max_calls_ahead,
            call_speed_multiplier,
            handbrake
    ):
        self.stage = stage
        self.voice = voice
        self.call_earliness = call_earliness
        self.max_calls_ahead = max_calls_ahead
        self.call_speed_multiplier = call_speed_multiplier
        self.handbrake = handbrake
        self.notes_list = []
        self.exit_all = False
        self.started = False
        self.restarted = False
        self.last_retrieve = time.time()
        self.speed_kmh = 0
        self.distance = 0
        self.time = 0

    def load_notes_list(self):
        self.notes_list = yaml.safe_load(open(f"pacenotes/{self.stage}.yml", encoding="utf-8"))
        if self.notes_list is None:
            self.notes_list = []

    def start(self):
        retrieve = Thread(target=self.retrieve_thread, daemon=True)
        speak = Thread(target=self.speak_thread, daemon=True)
        retrieve.start()
        speak.start()

    def retrieve_thread(self):
        asm = accSharedMemory()
        last_shared_memory = None

        previous_time = 0

        while not self.exit_all:
            sm = asm.read_shared_memory()
            if sm is None:
                sm = last_shared_memory

            if sm is not None:
                self.speed_kmh = sm.Physics.speed_kmh
                self.distance = sm.Graphics.distance_traveled
                previous_time = self.get_time() if self.get_time() != 0 else previous_time
                self.set_time(sm.Graphics.current_time_str)

                if self.time > 0 and previous_time > 0:
                    if self.time > previous_time:
                        # Detect whether player has set off from start line
                        self.started = True
                    elif previous_time > self.time:
                        # Detect whether a player has restarted
                        self.restarted = True

                last_shared_memory = sm
            else:
                continue
            time.sleep(0.05)

        asm.close()

    def speak_thread(self):
        token_sounds = self.build_token_sounds()
        self.load_notes_list()
        self.add_note_durations(self.notes_list, token_sounds)

        self.restarted = False

        while not self.exit_all and not self.started:
            time.sleep(0.1)

        util.play_beep()

        # Do not play too many notes ahead of time
        previous_distances = []

        stream = util.open_stream(next(iter(token_sounds.values()))[0])

        while len(self.notes_list) > 0 and not self.exit_all and not self.restarted:
            while len(previous_distances) > 0 and previous_distances[0] < self.distance:
                previous_distances.pop(0)

            if (len(previous_distances) < self.max_calls_ahead and self.notes_list[0]["distance"]
                    < self.distance +
                        (self.notes_list[0]["duration"] * (self.speed_kmh * (5/18))) +
                        (self.call_earliness * ((self.speed_kmh * (5/18))**self.call_speed_multiplier))):
                note = self.notes_list.pop(0)
                previous_distances.append(note["distance"])
                tokens = self.combine_tokens(note["notes"], token_sounds)
                link_to_next = note["link_to_next"]
                while link_to_next and len(self.notes_list) > 0:
                    next_note = self.notes_list.pop(0)
                    next_tokens = self.combine_tokens(next_note["notes"], token_sounds)
                    tokens.extend(next_tokens)
                    link_to_next = next_note["link_to_next"]

                self.play_tokens(stream, tokens, token_sounds)
            else:
                time.sleep(0.05)

        stream.close()

        if self.restarted:
            self.speak_thread()

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
                    sound_bytes = f.read()
                    token_sounds[token].append(sound_bytes)
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

    def play_tokens(self, stream, tokens, token_sounds):
        for token in tokens:
            # print(token)
            if token in token_sounds:
                sound = random.choice(token_sounds[token])
                util.play_audio(stream, sound)
            elif pause_time := self.match_pause(token):
                time.sleep(pause_time)

    def add_note_durations(self, notes_list, token_sounds):
        notes_list = notes_list.copy()
        while len(notes_list) > 0:
            note = notes_list.pop(0)
            note["duration"] = 0
            tokens = self.combine_tokens(note["notes"], token_sounds)
            link_to_next = note["link_to_next"]
            while link_to_next and len(notes_list) > 0:
                next_note = notes_list.pop(0)
                next_note["duration"] = 0
                next_tokens = self.combine_tokens(next_note["notes"], token_sounds)
                tokens.extend(next_tokens)
                link_to_next = next_note["link_to_next"]

            for token in tokens:
                if token in token_sounds:
                    with wave.open(io.BytesIO(token_sounds[token][0]), "rb") as f:
                        frames = f.getnframes()
                        rate = f.getframerate()
                        duration = frames / float(rate)
                        note["duration"] += duration
                elif pause_time := self.match_pause(token):
                    note["duration"] += pause_time

    def get_distance(self):
        return self.distance

    def set_time(self, value):
        try:
            value = str(value)
            # Format: 00:00.441\x00\x00\x00\x00\x00\x00
            value = int(value[0:2]) * 60 * 1000 + int(value[3:5]) * 1000 + int(value[6:9])
        except ValueError:
            value = 0
        self.time = value

    def get_time(self):
        return self.time

    def exit(self):
        self.exit_all = True
