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

conversion_pretty = {
    "DT_PacenoteHafrenNorthForwardCut1.json": "Cwmbiga - Fedw Fain",
    "DT_PacenoteHafrenNorthForwardCut2.json": "Banc Gwyn - Afon Biga",
    "DT_PacenoteHafrenNorthFullForward.json": "Cwmbiga - Afon Biga",
    "DT_PacenoteHafrenNorthFullReverse.json": "Afon Biga - Cwmbiga",
    "DT_PacenoteHafrenNorthReverseCut1.json": "Fedw Fain - Cwmbiga",
    "DT_PacenoteHafrenNorthReverseCut2.json": "Afon Biga - Banc Gwyn",
    "DT_PacenoteHafrenSouthForward.json": "Afon Bidno - Severn",
    "DT_PacenoteHafrenSouthReverse.json": "Severn - Afon Bidno",
    "DT_PacenoteMunsterFullForward.json": "Vallée de Munster Montée",
    "DT_PacenoteMunsterFullReverse.json": "Vallée de Munster Descente",
    "DT_PacenoteMunsterShort1Forward.json": "Luttenbach près Munster",
    "DT_PacenoteMunsterShort1Reverse.json": "Forêt de Munster",
    "DT_PacenoteMunsterShort2Forward.json": "Sommet de Munster",
    "DT_PacenoteMunsterShort2Reverse.json": "Col du petit Ballon",
    "DT_PacenoteSaverneCut1Forward.json": "Obersteigen",
    "DT_PacenoteSaverneCut1Reverse.json": "La traversée de La Mossig",
    "DT_PacenoteSaverneFullForward.json": "Forêt de Saverne",
    "DT_PacenoteSaverneFullReverse.json": "Steigenbach",
}

table_offset = {
    "DT_PacenoteHafrenNorthForwardCut1.json": 70,
    "DT_PacenoteHafrenNorthForwardCut2.json": 20,
    "DT_PacenoteHafrenNorthFullForward.json": 70,
    "DT_PacenoteHafrenNorthFullReverse.json": 30,
    "DT_PacenoteHafrenNorthReverseCut1.json": 50,
    "DT_PacenoteHafrenNorthReverseCut2.json": 30,
    "DT_PacenoteHafrenSouthForward.json": 70,
    "DT_PacenoteHafrenSouthReverse.json": 40,
    "DT_PacenoteMunsterFullForward.json": 20,
    "DT_PacenoteMunsterFullReverse.json": 30,
    "DT_PacenoteMunsterShort1Forward.json": 20,
    "DT_PacenoteMunsterShort1Reverse.json": 50,
    "DT_PacenoteMunsterShort2Forward.json": 30,
    "DT_PacenoteMunsterShort2Reverse.json": 20,
    "DT_PacenoteSaverneCut1Forward.json": 40,
    "DT_PacenoteSaverneCut1Reverse.json": 60,
    "DT_PacenoteSaverneFullForward.json": 20,
    "DT_PacenoteSaverneFullReverse.json": 60,
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
    offset = table_offset[key] - rows["R0000"]["SplineDistanceM"]
    for _, row in rows.items():
        distance = int(row["SplineDistanceM"] + offset)
        link_to_next = row["LinkToNext"]
        notes = row["TokenList"]["Tokens"]
        pacenotes.append({
            "distance": distance,
            "link_to_next": link_to_next,
            "notes": notes
        })
    yaml.dump(pacenotes, open(f"../pacenotes/{pretty_name}.yml", "w"), default_flow_style=None, sort_keys=False)
