import os.path
import random
import re
import time
from threading import Thread

import keyboard
import winsound
import yaml

from pyaccsharedmemory import accSharedMemory


class ACRally:
    def __init__(self, stage, voice, call_earliness, start_button):
        self.voice = voice
        self.call_earliness = call_earliness
        self.start_button = start_button
        self.notes_list = []
        self.exit_all = False
        self.started = False
        self.last_retrieve = time.time()
        self.speed_kmh = 0
        # Distance does not always start at 0
        self.distance = None

        self.notes_list = yaml.safe_load(open(f"pacenotes/{stage}.yml"))
        try:
            self.distance = self.notes_list[0]["distance"]
        except IndexError:
            self.distance = 0
        print(self.distance)

        retrieve = Thread(target=self.retrieve_thread, daemon=True)
        speak = Thread(target=self.speak_thread, daemon=True)
        retrieve.start()
        speak.start()

    def retrieve_thread(self):
        asm = accSharedMemory()
        last_shared_memory = None

        print(f"Press {self.start_button} when the countdown starts!")
        while not keyboard.is_pressed(self.start_button) and not self.exit_all:
            time.sleep(0.1)
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
        while not self.exit_all and not self.started:
            time.sleep(0.1)

        while len(self.notes_list) > 0 and not self.exit_all:
            if self.notes_list[0]["distance"] < self.distance + (120 + (self.speed_kmh // 2)) * self.call_earliness:
                note = self.notes_list.pop(0)
                tokens = note["notes"]
                # print(tokens)
                link_to_next = note["link_to_next"]
                while link_to_next:
                    next_note = self.notes_list.pop(0)
                    next_tokens = next_note["notes"]
                    tokens.extend(next_tokens)
                    link_to_next = next_note["link_to_next"]

                for token in tokens:
                    print(token)
                    if matches := re.match('Pause([\\d.]+)s(?:_Reset)?', token):
                        pause_time = float(matches.group(1))
                        print(f"Sleeping for {pause_time}")
                        time.sleep(pause_time)
                    else:
                        # This regex allows for After.wav and After_1.wav, etc.
                        files = [entry for entry in os.listdir(f"voices\\{self.voice}")
                                 if re.match(re.escape(token) + r'(?:_\d+)?\.wav', entry)]
                        if len(files) > 0:
                            filename = f"voices\\{self.voice}\\{random.choice(files)}"
                            winsound.PlaySound(filename, winsound.SND_FILENAME)

            else:
                time.sleep(0.1)
        print("Speak thread closed")

    def get_distance(self):
        return self.distance

    def exit(self):
        self.exit_all = True
