import os
import tkinter as tk
from tkinter import ttk

from acrally import ACRally


class Main:
    stages = None
    voices = None
    acrally = None
    btn_start = None
    btn_stop = None


    def on_button_start(self):
        print(self.stages.get())
        self.acrally = ACRally(str(self.voices.get()), str(self.stages.get()))
        self.btn_start["state"] = "disabled"
        self.btn_stop["state"] = "normal"


    def on_button_exit(self):
        if self.acrally:
            self.acrally.exit()
        self.btn_start["state"] = "normal"
        self.btn_stop["state"] = "disabled"

    def __init__(self):
        root = tk.Tk()
        root.title("AC Rally Pacenote Pal")
        root.geometry("340x300")

        stages = os.listdir("pacenotes")
        stages = [file.replace(".yml", "") for file in stages]

        ttk.Label(root, text="Select a stage:").pack(pady=(20, 5))
        self.stages = ttk.Combobox(root, values=stages, width=50)
        self.stages.pack(pady=5)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=20)

        self.btn_start = ttk.Button(btn_frame, text="Start", command=self.on_button_start)
        self.btn_start.pack(side=tk.LEFT, padx=10)

        self.btn_stop = ttk.Button(btn_frame, text="Stop", command=self.on_button_exit, state="disabled")
        self.btn_stop.pack(side=tk.LEFT, padx=10)

        ttk.Label(root, text="Click start and press the space bar when the countdown starts!").pack(pady=(20, 5))

        voices = os.listdir("voices")
        ttk.Label(root, text="Select a voice:").pack(pady=(20, 5))
        self.voices = ttk.Combobox(root, values=voices, width=50)
        self.voices.current(0)
        self.voices.pack(pady=5)

        root.mainloop()

if __name__ == '__main__':
    app = Main()
