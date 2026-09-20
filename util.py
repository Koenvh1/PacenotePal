import io
import os
import sys
import time
import wave
import tkinter as tk
from tkinter import ttk

import sounddevice


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def open_stream(audio_bytes):
    if type(audio_bytes) is bytes:
        audio_bytes = io.BytesIO(audio_bytes)
    with wave.open(audio_bytes, "rb") as wf:
        stream = sounddevice.RawOutputStream(samplerate=wf.getframerate(), channels=wf.getnchannels(), dtype="int16")
        stream.start()
        return stream


def play_audio(stream, audio_bytes):
    if type(audio_bytes) is bytes:
        audio_bytes = io.BytesIO(audio_bytes)
    with wave.open(audio_bytes, "rb") as wf:
        stream.write(wf.readframes(wf.getnframes()))


def play_beep():
    with open(str(resource_path("beep.wav")), "rb") as f:
        data = f.read()

        stream = open_stream(data)
        play_audio(stream, data)
        time.sleep(0.5)
        stream.close()


def initialise_audio():
    stream = sounddevice.RawOutputStream(samplerate=44100, channels=1, dtype="int16")
    stream.start()
    stream.close()


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.canvas = tk.Canvas(self, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.content_frame = ttk.Frame(self.canvas)

        self.content_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        canvas_frame = self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def get_content(self):
        return self.content_frame

    def get_scroll(self):
        return self.canvas.yview()[1]

    def set_scroll(self, previous_bottom):
        self.update_idletasks()
        new_top, new_bottom = self.canvas.yview()
        new_visible = new_bottom - new_top
        new_target_top = previous_bottom - new_visible
        new_target_top = max(0.0, min(1.0 - new_visible, new_target_top))
        self.canvas.yview_moveto(new_target_top)

