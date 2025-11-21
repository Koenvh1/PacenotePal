import itertools
import json
import yaml
import os.path

variants = json.load(open("DT_TracksVariants.json", encoding="utf-8"))[0]["Rows"]
for key, value in variants.items():
    print(value["StageName"]["Key"])
    continue

conversion_table = {
    "DT_PacenoteHafrenNorthForwardCut1.json": "TRACK_HAFRENNORTH_CUT1_FORWARD",
    "DT_PacenoteHafrenNorthForwardCut2.json": "TRACK_HAFRENNORTH_CUT2_FORWARD",
    "DT_PacenoteHafrenNorthFullForward.json": "TRACK_HAFRENNORTH_FULL_FORWARD",
    "DT_PacenoteHafrenNorthFullReverse.json": "TRACK_HAFRENNORTH_FULL_REVERSE",
    "DT_PacenoteHafrenNorthReverseCut1.json": "TRACK_HAFRENNORTH_CUT1_REVERSE",
    "DT_PacenoteHafrenNorthReverseCut2.json": "TRACK_HAFRENNORTH_CUT2_REVERSE",
    "DT_PacenoteHafrenSouthForward.json": "TRACK_HAFRENSOUTH_FULL_FORWARD",
    "DT_PacenoteHafrenSouthReverse.json": "TRACK_HAFRENSOUTH_FULL_REVERSE",
    "DT_PacenoteMunsterFullForward.json": "TRACK_MUNSTER_FULL_FORWARD",
    "DT_PacenoteMunsterFullReverse.json": "TRACK_MUNSTER_FULL_REVERSE",
    "DT_PacenoteMunsterShort1Forward.json": "TRACK_MUNSTER_SHORT1_FORWARD",
    "DT_PacenoteMunsterShort1Reverse.json": "TRACK_MUNSTER_SHORT1_REVERSE",
    "DT_PacenoteMunsterShort2Forward.json": "TRACK_MUNSTER_SHORT2_FORWARD",
    "DT_PacenoteMunsterShort2Reverse.json": "TRACK_MUNSTER_SHORT2_REVERSE",
    "DT_PacenoteSaverneCut1Forward.json": "TRACK_SAVERNE_SHORT1_FORWARD",
    "DT_PacenoteSaverneCut1Reverse.json": "TRACK_SAVERNE_SHORT1_REVERSE",
    "DT_PacenoteSaverneFullForward.json": "TRACK_SAVERNE_FULL_FORWARD",
    "DT_PacenoteSaverneFullReverse.json": "TRACK_SAVERNE_FULL_REVERSE",
}

def get_pretty_name(key):
    global variants
    for k, v in variants.items():
        if v["StageName"]["Key"] == key:
            return v["StageName"]["SourceString"].strip()
    return None

for key, value in conversion_table.items():
    pretty_name = get_pretty_name(value)

    data = json.load(open("../pacenotes_raw/" + key))
    rows = data[0]["Rows"]


    pacenotes = []
    for _, row in rows.items():
        distance = row["SplineDistanceM"]
        link_to_next = row["LinkToNext"]
        notes = row["TokenList"]["Tokens"]
        pacenotes.append({
            "distance": distance,
            "link_to_next": link_to_next,
            "notes": notes
        })
    yaml.dump(pacenotes, open(f"../pacenotes/{pretty_name}.yml", "w"), default_flow_style=None, sort_keys=False)
