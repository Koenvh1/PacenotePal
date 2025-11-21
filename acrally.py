import os.path
import re
import time
from threading import Thread

import keyboard
import winsound
import yaml

from pyaccsharedmemory import accSharedMemory


class ACRally:
    def __init__(self, voice, stage, call_earliness):
        self.voice = voice
        self.call_earliness = call_earliness
        self.notes_list = []
        self.exit_all = False
        self.started = False
        self.last_retrieve = time.time()
        self.speed_kmh = 0
        # Distance does not always start at 0
        self.distance = None

        self.notes_list = yaml.safe_load(open(f"pacenotes/{stage}.yml"))
        self.distance = self.notes_list[0]["distance"]
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
                        filename = f"voices\\{self.voice}\\{token}.wav"
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
