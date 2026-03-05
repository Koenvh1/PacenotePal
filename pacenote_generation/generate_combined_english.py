import collections
import json
import os

import yaml


def to_dict(tsv):
    d = {}
    for line in tsv:
        line = line.strip()
        key, value = line.split("\t", 1)
        d[key] = value
    return d

output = open("pacenotes_combined_english.tsv", "w", encoding="utf-8")

to_generate = []
translation = to_dict(open("pacenotes_english.tsv", encoding="utf-8"))
for file in os.listdir("../pacenotes"):
    pacenotes = yaml.safe_load(open("../pacenotes/" + file))
    for pacenote in pacenotes:
        notes = pacenote["notes"]
        new_notes = []
        for note in notes:
            if not "Pause" in note:
                new_notes.append(note)
            else:
                if len(new_notes) > 0:
                    to_generate.append("-".join(new_notes))
                    new_notes = []
        to_generate.append("-".join(new_notes))

details = json.load(open("DT_PacenoteTokens_EA.json"))[0]["Rows"]

to_generate = sorted(list(set(to_generate)))
for entry in to_generate:
    notes = entry.split("-")
    if len(notes) >= 2:
        combined = " ".join([(f'<emphasis level="strong">{translation.get(x, "")}</emphasis>' if x in details and details[x]["Category"] not in ["Conjunctions"] else translation.get(x, "")) for x in notes])
        output.write(f"{entry}\t{combined.lower()}\n")