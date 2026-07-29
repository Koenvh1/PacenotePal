import json
import os

import yaml

import process_acr_pacenote_files


stage_map = {}

base_data = json.load(open("stages/en/Game.json", encoding="utf-8"))[""]
for language in os.listdir("stages"):
    data = json.load(open("stages/" + language + "/Game.json", encoding="utf-8"))[""]

    def get_data(key):
        if key in data:
            return data[key]
        else:
            return base_data[key]

    for key, value in process_acr_pacenote_files.conversion_table.items():
        file_name = process_acr_pacenote_files.get_pretty_name(value[0])
        mmap_name = get_data(value[1]) + " " + get_data(process_acr_pacenote_files.get_short_name_key(value[0]))
        stage_map[mmap_name] = file_name
        if len(mmap_name) > 32:
            stage_map[mmap_name[:32]] = file_name

yaml.dump(stage_map, open("../stages.yml", "w", encoding="utf-8"), width=1024, allow_unicode=True)
