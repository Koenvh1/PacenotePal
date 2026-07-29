import itertools
import json
import yaml
import os.path

variants = json.load(open("DT_TracksVariants.json", encoding="utf-8"))[0]["Rows"]
for key, value in variants.items():
    print(value["StageName"]["Key"])
    continue

conversion_table = {
    "DT_PacenoteBolleneCut1Forward.json": ("TRACK_COLDETURINI_SHORT1_FORWARD", "TRACK_LOCATION_MONTECARLO"),
    "DT_PacenoteBolleneCut1Reverse.json": ("TRACK_COLDETURINI_SHORT1_REVERSE", "TRACK_LOCATION_MONTECARLO"),
    "DT_PacenoteBolleneCut2Forward.json": ("TRACK_COLDETURINI_SHORT2_FORWARD", "TRACK_LOCATION_MONTECARLO"),
    "DT_PacenoteBolleneCut2Reverse.json": ("TRACK_COLDETURINI_SHORT2_REVERSE", "TRACK_LOCATION_MONTECARLO"),
    "DT_PacenoteBolleneCut3Forward.json": ("TRACK_COLDETURINI_SHORT3_FORWARD", "TRACK_LOCATION_MONTECARLO"),
    "DT_PacenoteBolleneCut3Reverse.json": ("TRACK_COLDETURINI_SHORT3_REVERSE", "TRACK_LOCATION_MONTECARLO"),
    "DT_PacenoteBolleneFullForward.json": ("TRACK_COLDETURINI_FULL_FORWARD", "TRACK_LOCATION_MONTECARLO"),
    "DT_PacenoteBolleneFullReverse.json": ("TRACK_COLDETURINI_FULL_REVERSE", "TRACK_LOCATION_MONTECARLO"),

    "DT_PacenoteHafrenNorthForwardCut1.json": ("TRACK_HAFRENNORTH_CUT1_FORWARD", "TRACK_LOCATION_WALES"),
    "DT_PacenoteHafrenNorthForwardCut2.json": ("TRACK_HAFRENNORTH_CUT2_FORWARD", "TRACK_LOCATION_WALES"),
    "DT_PacenoteHafrenNorthFullForward.json": ("TRACK_HAFRENNORTH_FULL_FORWARD", "TRACK_LOCATION_WALES"),
    "DT_PacenoteHafrenNorthFullReverse.json": ("TRACK_HAFRENNORTH_FULL_REVERSE", "TRACK_LOCATION_WALES"),
    "DT_PacenoteHafrenNorthReverseCut1.json": ("TRACK_HAFRENNORTH_CUT1_REVERSE", "TRACK_LOCATION_WALES"),
    "DT_PacenoteHafrenNorthReverseCut2.json": ("TRACK_HAFRENNORTH_CUT2_REVERSE", "TRACK_LOCATION_WALES"),
    "DT_PacenoteHafrenSouthForward.json": ("TRACK_HAFRENSOUTH_FULL_FORWARD", "TRACK_LOCATION_WALES"),
    "DT_PacenoteHafrenSouthReverse.json": ("TRACK_HAFRENSOUTH_FULL_REVERSE", "TRACK_LOCATION_WALES"),

    "DT_PacenoteMunsterFullForward.json": ("TRACK_MUNSTER_FULL_FORWARD", "TRACK_LOCATION_ALSACE"),
    "DT_PacenoteMunsterFullReverse.json": ("TRACK_MUNSTER_FULL_REVERSE", "TRACK_LOCATION_ALSACE"),
    "DT_PacenoteMunsterShort1Forward.json": ("TRACK_MUNSTER_SHORT1_FORWARD", "TRACK_LOCATION_ALSACE"),
    "DT_PacenoteMunsterShort1Reverse.json": ("TRACK_MUNSTER_SHORT1_REVERSE", "TRACK_LOCATION_ALSACE"),
    "DT_PacenoteMunsterShort2Forward.json": ("TRACK_MUNSTER_SHORT2_FORWARD", "TRACK_LOCATION_ALSACE"),
    "DT_PacenoteMunsterShort2Reverse.json": ("TRACK_MUNSTER_SHORT2_REVERSE", "TRACK_LOCATION_ALSACE"),
    "DT_PacenoteSaverneCut1Forward.json": ("TRACK_SAVERNE_SHORT1_FORWARD", "TRACK_LOCATION_ALSACE"),
    "DT_PacenoteSaverneCut1Reverse.json": ("TRACK_SAVERNE_SHORT1_REVERSE", "TRACK_LOCATION_ALSACE"),
    "DT_PacenoteSaverneFullForward.json": ("TRACK_SAVERNE_FULL_FORWARD", "TRACK_LOCATION_ALSACE"),
    "DT_PacenoteSaverneFullReverse.json": ("TRACK_SAVERNE_FULL_REVERSE", "TRACK_LOCATION_ALSACE"),

    "DT_PacenoteSisteronCut1Forward.json": ("TRACK_SISTERON_CUT1_FORWARD", "TRACK_LOCATION_MONTECARLO"),
    "DT_PacenoteSisteronCut1Reverse.json": ("TRACK_SISTERON_CUT1_REVERSE", "TRACK_LOCATION_MONTECARLO"),
    "DT_PacenoteSisteronCut2Forward.json": ("TRACK_SISTERON_CUT2_FORWARD", "TRACK_LOCATION_MONTECARLO"),
    "DT_PacenoteSisteronCut2Reverse.json": ("TRACK_SISTERON_CUT2_REVERSE", "TRACK_LOCATION_MONTECARLO"),
    "DT_PacenoteSisteronFullForward.json": ("TRACK_SISTERON_FULL_FORWARD", "TRACK_LOCATION_MONTECARLO"),
    "DT_PacenoteSisteronFullReverse.json": ("TRACK_SISTERON_FULL_REVERSE", "TRACK_LOCATION_MONTECARLO"),

    "DT_PacenoteElatiaCut1Forward.json": ("TRACK_ELATIA_CUT1_FORWARD", "TRACK_LOCATION_GRECE"),
    "DT_PacenoteElatiaCut1Reverse.json": ("TRACK_ELATIA_CUT1_REVERSE", "TRACK_LOCATION_GRECE"),
    "DT_PacenoteElatiaCut2Forward.json": ("TRACK_ELATIA_CUT2_FORWARD", "TRACK_LOCATION_GRECE"),
    "DT_PacenoteElatiaCut2Reverse.json": ("TRACK_ELATIA_CUT2_REVERSE", "TRACK_LOCATION_GRECE"),
    "DT_PacenoteElatiaFullForward.json": ("TRACK_ELATIA_FULL_FORWARD", "TRACK_LOCATION_GRECE"),
    "DT_PacenoteElatiaFullReverse.json": ("TRACK_ELATIA_FULL_REVERSE", "TRACK_LOCATION_GRECE"),

    "DT_PacenoteLoutrakiCut1Forward.json": ("TRACK_LOUTRAKI_CUT1_FORWARD", "TRACK_LOCATION_GRECE"),
    "DT_PacenoteLoutrakiCut1Reverse.json": ("TRACK_LOUTRAKI_CUT1_REVERSE", "TRACK_LOCATION_GRECE"),
    "DT_PacenoteLoutrakiCut2Forward.json": ("TRACK_LOUTRAKI_CUT2_FORWARD", "TRACK_LOCATION_GRECE"),
    "DT_PacenoteLoutrakiCut2Reverse.json": ("TRACK_LOUTRAKI_CUT2_REVERSE", "TRACK_LOCATION_GRECE"),
    "DT_PacenoteLoutrakiFullForward.json": ("TRACK_LOUTRAKI_FULL_FORWARD", "TRACK_LOCATION_GRECE"),
    "DT_PacenoteLoutrakiFullReverse.json": ("TRACK_LOUTRAKI_FULL_REVERSE_SHORT", "TRACK_LOCATION_GRECE"),
}


def get_pretty_name(key):
    global variants
    for k, v in variants.items():
        if v["StageName"]["Key"] == key:
            return v["StageName"]["SourceString"].strip()
    return None

def get_short_name_key(key):
    global variants
    for k, v in variants.items():
        if v["StageName"]["Key"] == key:
            return v["Name"]["Key"].strip()
    return None

for key, value in conversion_table.items():
    pretty_name = get_pretty_name(value[0])

    data = json.load(open("../pacenotes_raw/" + key))
    rows = data[0]["Rows"]

    pacenotes = []
    for _, row in rows.items():
        distance = int(row["SplineDistanceM"]) # + offset
        link_to_next = row["LinkToNext"]
        notes = row["TokenList"]["Tokens"]
        pacenotes.append({
            "distance": distance,
            "link_to_next": link_to_next,
            "notes": notes
        })
    yaml.dump(pacenotes, open(f"../pacenotes/{pretty_name}.yml", "w"), default_flow_style=None, sort_keys=False)
