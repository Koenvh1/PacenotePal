import os
import threading
import time
import tkinter as tk
from tkinter import ttk

import yaml

import util
from acrally import ACRally
from editor import Editor


class Main:
    root = None
    stages = None
    voices = None
    call_earliness = None
    acrally = None
    btn_start = None
    btn_stop = None
    config = None


    def on_button_start(self):
        print(self.stages.get())
        self.acrally = ACRally(
            str(self.stages.get()),
            self.config.get("voice", "English"),
            float(self.config.get("call_distance", 1.0)),
            int(self.config.get("calls_ahead", 3)),
            float(self.config.get("call_speed_multiplier", 1.0)),
            self.config.get("start_button", "space"),
            self.config.get("handbrake", None)
        )
        self.acrally.start()
        self.btn_start["state"] = "disabled"
        self.btn_stop["state"] = "normal"


    def on_button_exit(self):
        if self.acrally:
            self.acrally.exit()
        self.btn_start["state"] = "normal"
        self.btn_stop["state"] = "disabled"

    def on_button_distance(self):
        distance_window = tk.Toplevel(self.root)
        distance_window.title("Odometer")
        distance_window.iconbitmap(util.resource_path("icon.ico"))
        distance_window.geometry("200x100")
        distance_window.attributes("-topmost", True)
        distance_var = tk.StringVar()
        distance_var.set("----")
        distance_label = ttk.Label(distance_window, textvariable=distance_var, font=("sans-serif", 40))
        distance_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        stop = False

        def retrieve_distance():
            nonlocal stop
            while not stop:
                if self.acrally:
                    if distance := self.acrally.get_distance():
                        distance_var.set(str(int(distance)))
                    else:
                        distance_var.set("----")
                time.sleep(0.05)

        def on_close():
            nonlocal stop
            stop = True
            distance_window.destroy()

        worker = threading.Thread(target=retrieve_distance, daemon=True)
        worker.start()
        distance_window.protocol("WM_DELETE_WINDOW", on_close)

    def on_button_pacenotes(self):
        editor = Editor()
        editor.main()

    def on_button_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.iconbitmap(util.resource_path("icon.ico"))
        settings_window.geometry("280x390")

        settings_frame = ttk.Frame(settings_window)
        settings_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(settings_frame, text="Voice").grid(column=0, row=0, padx=5, pady=5)
        voice_var = tk.StringVar(value=self.config.get("voice", "English"))
        voice_combo = ttk.Combobox(settings_frame, values=[x.strip() for x in os.listdir("voices")], textvariable=voice_var)
        voice_combo.grid(column=1, row=0, padx=5, pady=5)

        ttk.Label(settings_frame, text="Call distance").grid(column=0, row=1, padx=5, pady=5)
        call_distance_var = tk.DoubleVar(value=self.config.get("call_distance", 1.0))
        call_distance_spinbox = ttk.Spinbox(settings_frame, textvariable=call_distance_var, from_=0.1, to=5.0, increment=0.1)
        call_distance_spinbox.grid(column=1, row=1, padx=5, pady=5)

        ttk.Label(settings_frame, text="Multiplier for the call distance:\n"
                                       "2.0 makes the calls twice as early,\n"
                                       "0.5 makes the calls twice as late."
                  ).grid(column=0, columnspan=2, row=2, sticky="W")

        ttk.Label(settings_frame, text="Calls ahead").grid(column=0, row=3, padx=5, pady=5)
        calls_ahead_var = tk.IntVar(value=self.config.get("calls_ahead", 3))
        calls_ahead_spinbox = ttk.Spinbox(settings_frame, textvariable=calls_ahead_var, from_=1, to=10, increment=1)
        calls_ahead_spinbox.grid(column=1, row=3, padx=5, pady=5)

        ttk.Label(settings_frame, text="The maximum number of notes you want to\n"
                                       "hear coming up that you have not passed yet."
                  ).grid(column=0, columnspan=2, row=4, sticky="W")

        ttk.Label(settings_frame, text="Speed multiplier").grid(column=0, row=5, padx=5, pady=5)
        call_speed_multiplier_var = tk.DoubleVar(value=self.config.get("call_speed_multiplier", 1.0))
        call_speed_multiplier_spinbox = ttk.Spinbox(settings_frame, textvariable=call_speed_multiplier_var, from_=0.0, to=5.0, increment=0.1)
        call_speed_multiplier_spinbox.grid(column=1, row=5, padx=5, pady=5)

        ttk.Label(settings_frame, text="The multiplier for how much earlier the call\n"
                                       "is made with higher speeds.\n"
                                       "2.0 makes the speed twice as influential,\n"
                                       "0.0 disables the speed influence entirely."
                  ).grid(column=0, columnspan=2, row=6, sticky="W")

        ttk.Label(settings_frame, text="Start button").grid(column=0, row=7, padx=5, pady=5)
        start_var = tk.StringVar(value=self.config.get("start_button", "space"))
        start_entry = ttk.Entry(settings_frame, textvariable=start_var)
        start_entry.grid(column=1, row=7, padx=5, pady=5)
        def start_entry_key(e):
            TK_TO_KEYBOARD = {
                "Return": "enter",
                "BackSpace": "backspace",
                "Tab": "tab",
                "Escape": "esc",
                "Shift_L": "shift",
                "Shift_R": "shift",
                "Control_L": "ctrl",
                "Control_R": "ctrl",
                "Alt_L": "alt",
                "Alt_R": "alt",
                "space": "space",
                "Left": "left",
                "Right": "right",
                "Up": "up",
                "Down": "down",
                "Delete": "delete",
                "Insert": "insert",
                "Home": "home",
                "End": "end",
                "Prior": "page up",
                "Next": "page down",
            }

            def tk_to_keyboard(event):
                if event.keysym in TK_TO_KEYBOARD:
                    return TK_TO_KEYBOARD[event.keysym]

                if event.char and event.char.isprintable():
                    return event.char.lower()

                if event.keysym.startswith("F") and event.keysym[1:].isdigit():
                    return event.keysym.lower()

                return event.keysym.lower()

            start_var.set(tk_to_keyboard(e))
        start_entry.bind("<KeyRelease>", start_entry_key)

        ttk.Label(settings_frame, text="Button to press at the start of the stage.\n"
                                       "See the README to use your handbrake instead."
                  ).grid(column=0, columnspan=2, row=8, sticky="W")

        def save():
            self.config["voice"] = voice_var.get()
            self.config["start_button"] = start_var.get()
            self.config["call_distance"] = call_distance_var.get()
            self.config["calls_ahead"] = calls_ahead_var.get()
            self.config["call_speed_multiplier"] = call_speed_multiplier_var.get()
            yaml.dump(self.config, open("config.yml", "w"))
            settings_window.withdraw()

        save_btn = ttk.Button(settings_frame, text="Save", command=save)
        save_btn.grid(column=0, columnspan=2, row=9, padx=5, pady=5)

    def __init__(self):
        self.config = yaml.safe_load(open("config.yml"))

        root = tk.Tk()
        root.title("AC Rally Pacenote Pal")
        root.iconbitmap(util.resource_path("icon.ico"))
        root.geometry("340x230")
        self.root = root

        stages = os.listdir("pacenotes")
        stages = [file.replace(".yml", "") for file in stages]

        ttk.Label(root, text="Select a stage:").pack(pady=(20, 5))
        self.stages = ttk.Combobox(root, values=stages, width=50)
        self.stages.pack(pady=5, padx=15, fill="x")

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        self.btn_start = ttk.Button(btn_frame, text="Start", command=self.on_button_start)
        self.btn_start.pack(side=tk.LEFT, padx=10)

        self.btn_stop = ttk.Button(btn_frame, text="Stop", command=self.on_button_exit, state="disabled")
        self.btn_stop.pack(side=tk.LEFT, padx=10)

        btn_distance = ttk.Button(btn_frame, text="Odometer", command=self.on_button_distance)
        btn_distance.pack(side=tk.LEFT, padx=10)

        ttk.Label(root, text=f"Click start and press {self.config.get("start_button", "space")} when the countdown starts!").pack(pady=(20, 5))

        btn_frame2 = tk.Frame(root)
        btn_frame2.pack(pady=10)

        btn_editor = ttk.Button(btn_frame2, text="Pacenote Editor", command=self.on_button_pacenotes)
        btn_editor.pack(side=tk.LEFT, padx=10)

        btn_settings = ttk.Button(btn_frame2, text="Settings", command=self.on_button_settings)
        btn_settings.pack(side=tk.LEFT, padx=10)

        root.mainloop()

if __name__ == '__main__':
    app = Main()
