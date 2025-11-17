import json
import os.path
import random
import re
import time
from threading import Thread

import keyboard
import winsound

from pyaccsharedmemory import accSharedMemory


class ACRally:
    def __init__(self, stage):
        self.call_earliness = 120
        self.notes_list = []
        self.exit_all = False
        self.started = False
        self.last_retrieve = time.time()
        self.speed_kmh = 0
        # Distance does not always start at 0
        self.distance = None

        notes = json.load(open(f"pacenotes/{stage}.json"))[0]["Rows"]
        for k, v in notes.items():
            self.notes_list.append(v)
        self.distance = self.notes_list[0]["SplineDistanceM"]
        print(self.distance)

        retrieve = Thread(target=self.retrieve_thread, daemon=True)
        speak = Thread(target=self.speak_thread, daemon=True)
        retrieve.start()
        speak.start()

    def retrieve_thread(self):
        asm = accSharedMemory()
        last_shared_memory = None

        print("Press the space bar when the countdown starts!")
        while not keyboard.is_pressed("space") and not self.exit_all:
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
        # engine = pyttsx3.init()
        # initial_distance = distance
        # while distance - initial_distance < 170:
        #     # Do not immediately blurt out everything before the start of the stage
        #     time.sleep(0.1)

        while not self.exit_all and not self.started:
            time.sleep(0.1)

        while len(self.notes_list) > 0 and not self.exit_all:
            if self.notes_list[0]["SplineDistanceM"] < self.distance + self.call_earliness + (self.speed_kmh // 2):
                note = self.notes_list.pop(0)
                tokens = note["TokenList"]["Tokens"]
                # print(tokens)
                link_to_next = note["LinkToNext"]
                while link_to_next:
                    next_note = self.notes_list.pop(0)
                    next_tokens = next_note["TokenList"]["Tokens"]
                    tokens.extend(next_tokens)
                    link_to_next = next_note["LinkToNext"]

                for token in tokens:
                    print(token)
                    if matches := re.match('Pause([\\d.]+)s(?:_Reset)?', token):
                        pause_time = float(matches.group(1))
                        print(f"Sleeping for {pause_time}")
                        time.sleep(pause_time)
                    else:
                        filename = f"voices\\{token}.wav"
                        if os.path.exists(filename):
                            winsound.PlaySound(filename, winsound.SND_FILENAME)
                        # files = [entry for entry in os.listdir("voices") if entry.startswith(token)]
                        # if len(files) > 0:
                        #     filename = f"voices\\{random.choice(files)}"
                        #     winsound.PlaySound(filename, winsound.SND_FILENAME)
                    # engine.say(token)
                # engine.runAndWait()
            else:
                time.sleep(0.1)
        print("Speak thread closed")

    def exit(self):
        self.exit_all = True
