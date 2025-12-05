import os
import threading
import tkinter as tk
import tkinter.messagebox as mb
from tkinter import ttk

import yaml

import util
from acrally import ACRally


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        canvas = tk.Canvas(self, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas_frame = canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

class Editor:
    def __init__(self):
        self.scroll_frame = None
        self.pacenotes_combo = None
        self.voices_combo = None
        self.load_button = None
        self.save_button = None
        self.new_button = None

        self.acrally = None
        self.pacenote_elements = []
        self.pacenote_vars = []

        self.token_sounds = None
        self.pacenotes = None
        self.pacenote_options = []

    def load(self):
        self.acrally = ACRally(
            self.pacenotes_combo.get(),
            self.voices_combo.get(),
            1,
            None,
            None
        )
        self.token_sounds = self.acrally.build_token_sounds()
        self.pacenote_options = [x for x in self.token_sounds.keys() if "-" not in x]
        self.pacenote_options.extend(["Pause0.1s", "Pause0.25s", "Pause0.5s", "Pause1.0s", "Pause1.5s"])
        self.save_button["state"] = "normal"
        self.draw_pacenotes_frame()

    def new_pacenotes(self):
        if self.pacenotes:
            res = mb.askyesno("New Pacenotes", "Are you sure you want to start from a blank slate? "
                                                "All unsaved changed will be lost!")
            if not res:
                return
        self.pacenotes = []
        self.load()

    def load_pacenotes(self):
        if self.pacenotes:
            res = mb.askyesno("Load Pacenotes", "Are you sure you want to load these pacenotes? "
                                                "All unsaved changed will be lost!")
            if not res:
                return
        self.pacenotes = yaml.safe_load(open(f"pacenotes/{self.pacenotes_combo.get()}.yml"))
        self.load()

    def save_pacenotes(self):
        res = mb.askyesno("Save Pacenotes",
                          f"Are you sure you want to save your pacenotes to \"{self.pacenotes_combo.get()}.yml\"? "
                          f"Existing content will be overwritten!")

        if res:
            yaml.dump(
                self.pacenotes,
                open(f"pacenotes/{self.pacenotes_combo.get()}.yml", "w"),
                default_flow_style=None,
                sort_keys=False
            )

    def draw_pacenotes_frame(self):
        [x.destroy() for x in self.pacenote_elements]
        self.pacenote_elements = []
        self.pacenote_vars = []

        def draw_pacenotes(i, pacenote):
            def pacenote_remove(i=i):
                self.pacenotes.pop(i)
                self.draw_pacenotes_frame()
            remove_btn = ttk.Button(self.scroll_frame.scrollable_frame, text="🗙", width=3, command=pacenote_remove)
            remove_btn.grid(row=i, column=0, padx=5, pady=5)
            self.pacenote_elements.append(remove_btn)

            distance_var = tk.StringVar(value=str(int(pacenote["distance"])))
            distance_entry = ttk.Entry(self.scroll_frame.scrollable_frame, textvariable=distance_var, width=6)
            distance_entry.grid(row=i, column=1, padx=5, pady=5)
            self.pacenote_elements.append(distance_entry)

            def distance_change(e, i=i):
                distance = distance_var.get().strip()
                if distance.isdigit():
                    key = lambda x: x["distance"]
                    self.pacenotes[i]["distance"] = int(distance)
                    sorted_list = sorted(self.pacenotes, key=key)
                    if self.pacenotes != sorted_list:
                        self.pacenotes.sort(key=key)
                        self.draw_pacenotes_frame()
            distance_entry.bind("<FocusOut>", distance_change)
            distance_entry.bind("<Return>", distance_change)
            # self.pacenote_vars.append(distance_var)

            link_var = tk.BooleanVar(value=pacenote["link_to_next"])
            def link_change(index, value, op, i=i):
                self.pacenotes[i]["link_to_next"] = link_var.get()
            link_var.trace("w", link_change)
            link_chk = ttk.Checkbutton(
                self.scroll_frame.scrollable_frame,
                variable=link_var,
                text="Link to next"
            )
            link_chk.grid(row=i, column=2, padx=5, pady=5)
            self.pacenote_elements.append(link_chk)
            self.pacenote_vars.append(link_var)

            pacenotes_frame = None
            combined_pacenotes_frame = None

            def draw_pacenotes(
                    i=i
            ):
                nonlocal pacenotes_frame
                if pacenotes_frame:
                    pacenotes_frame.destroy()
                pacenotes_frame = ttk.Frame(self.scroll_frame.scrollable_frame)
                pacenotes_frame.grid(row=i, column=3, padx=5, pady=5, sticky="w")

                def create_entry(note_idx, t):
                    note_var = tk.StringVar(value=t)
                    note_combo = ttk.Combobox(
                        pacenotes_frame,
                        values=self.pacenote_options,
                        textvariable=note_var
                    )
                    note_combo.grid(row=note_idx, column=0)
                    note_combo.unbind_class("TCombobox", "<MouseWheel>")

                    def note_change(e, note_idx=note_idx):
                        new_note = note_var.get()
                        old_note = self.pacenotes[i]["notes"][note_idx]
                        if old_note != new_note:
                            self.pacenotes[i]["notes"][note_idx] = new_note
                            draw_playable_pacenotes(
                                i
                            )
                    note_combo.bind("<FocusOut>", note_change)
                    note_combo.bind("<<ComboboxSelected>>", note_change)
                    note_combo.bind("<Return>", note_change)
                    self.pacenote_vars.append(note_var)

                    def note_up(note_idx=note_idx):
                        self.pacenotes[i]["notes"].insert(note_idx - 1, self.pacenotes[i]["notes"].pop(note_idx))
                        draw_pacenotes(
                            i
                        )

                    note_up = ttk.Button(pacenotes_frame, text="▲", width=3, command=note_up)
                    note_up.grid(row=note_idx, column=1)
                    if note_idx == 0:
                        note_up["state"] = "disabled"

                    def note_down(note_idx=note_idx):
                        self.pacenotes[i]["notes"].insert(note_idx + 1, self.pacenotes[i]["notes"].pop(note_idx))
                        draw_pacenotes(
                            i
                        )

                    note_down = ttk.Button(pacenotes_frame, text="▼", width=3, command=note_down)
                    note_down.grid(row=note_idx, column=2)
                    if note_idx == len(pacenote["notes"]) - 1:
                        note_down["state"] = "disabled"

                    def note_remove(note_idx=note_idx):
                        self.pacenotes[i]["notes"].pop(note_idx)
                        draw_pacenotes(
                            i
                        )

                    note_remove = ttk.Button(pacenotes_frame, text="🗙", width=3, command=note_remove)
                    note_remove.grid(row=note_idx, column=3)

                for note_idx, t in enumerate(pacenote["notes"]):
                    create_entry(note_idx, t)

                def add_note(i=i):
                    self.pacenotes[i]["notes"].append("")
                    draw_pacenotes(
                        i
                    )
                add_button = ttk.Button(pacenotes_frame, text="+ Add", command=add_note)
                add_button.grid(row=len(pacenote["notes"]), column=1, columnspan=3)
                self.pacenote_elements.append(pacenotes_frame)
                draw_playable_pacenotes(
                    i
                )

            def draw_playable_pacenotes(
                    i=i
            ):
                nonlocal combined_pacenotes_frame
                if combined_pacenotes_frame:
                    combined_pacenotes_frame.destroy()
                playable_tokens = self.acrally.combine_tokens(self.pacenotes[i]["notes"], self.token_sounds)
                combined_pacenotes_frame = ttk.Frame(self.scroll_frame.scrollable_frame)
                combined_pacenotes_frame.grid(row=i, column=4, padx=5, pady=5, sticky="w")
                for t in playable_tokens:
                    lbl = ttk.Label(combined_pacenotes_frame, text=t)
                    lbl.pack(anchor="w")
                    if pause := self.acrally.match_pause(t):
                        lbl["text"] = f"Pause {pause} seconds"
                        lbl["foreground"] = "blue"
                    elif t not in self.token_sounds:
                        lbl["foreground"] = "red"
                def play(t=playable_tokens):
                    threading.Thread(target=self.acrally.play_tokens, args=(t, self.token_sounds), daemon=True).start()
                play_btn = ttk.Button(combined_pacenotes_frame, text="▶ Play", command=play)
                play_btn.pack(anchor="w")
                self.pacenote_elements.append(play_btn)
                self.pacenote_elements.append(combined_pacenotes_frame)

            draw_pacenotes()

        for i, pacenote in enumerate(self.pacenotes):
            draw_pacenotes(i, pacenote)

        def swap_rows(r1, r2):
            row1 = self.scroll_frame.scrollable_frame.grid_slaves(row=r1)
            row2 = self.scroll_frame.scrollable_frame.grid_slaves(row=r2)

            for w in row1:
                w.grid(row=r2)

            for w in row2:
                w.grid(row=r1)

        def pacenote_add():
            self.pacenotes.append({
                "distance": 0,
                "link_to_next": False,
                "notes": [""]
            })
            add_btn.grid(row=len(self.pacenotes))
            draw_pacenotes(len(self.pacenotes) - 1, self.pacenotes[len(self.pacenotes) - 1])
        add_btn = ttk.Button(self.scroll_frame.scrollable_frame, text="+ Add pacenote", command=pacenote_add)
        add_btn.grid(row=len(self.pacenotes), column=1, columnspan=2, padx=5, pady=5)
        self.pacenote_elements.append(add_btn)

    def main(self):
        root = tk.Toplevel()
        root.title("AC Rally Pacenote Pal editor")
        root.iconbitmap(util.resource_path("icon.ico"))
        root.geometry("650x600")

        top_frame = ttk.Frame(root, padding=10)
        top_frame.pack(fill="x")

        self.pacenotes_combo = ttk.Combobox(
            top_frame,
            values=[x.replace(".yml", "") for x in os.listdir("pacenotes")],
            width=25
        )
        self.voices_combo = ttk.Combobox(top_frame, values=[x for x in os.listdir("voices")])
        self.pacenotes_combo.current(0)
        self.voices_combo.current(0)

        self.pacenotes_combo.grid(row=0, column=0, padx=5, pady=5)
        self.voices_combo.grid(row=0, column=1, padx=5, pady=5)

        self.load_button = ttk.Button(top_frame, text="Load", command=self.load_pacenotes)
        self.load_button.grid(row=0, column=2, padx=5, pady=5)

        self.save_button = ttk.Button(top_frame, text="Save", command=self.save_pacenotes)
        self.save_button.grid(row=0, column=3, padx=5, pady=5)
        self.save_button["state"] = "disabled"

        self.new_button = ttk.Button(top_frame, text="New", command=self.new_pacenotes)
        self.new_button.grid(row=0, column=4, padx=5, pady=5)

        # Scrollable frame
        self.scroll_frame = ScrollableFrame(root)
        self.scroll_frame.pack(fill="both", expand=True)

        root.mainloop()

if __name__ == "__main__":
    editor = Editor()
    editor.main()
