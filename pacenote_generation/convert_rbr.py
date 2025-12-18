import os
import re

conversion = {
    # Basic corners
    "Left1": "one_left",
    "Left2": "two_left",
    "Left3": "three_left",
    "Left4": "four_left",
    "Left5": "five_left",
    "Left6": "six_left",

    "Right1": "one_right",
    "Right2": "two_right",
    "Right3": "three_right",
    "Right4": "four_right",
    "Right5": "five_right",
    "Right6": "six_right",

    # Direction changes
    "LeftRight": "left_right",
    "RightLeft": "right_left",

    # Hairpins
    "LeftAcuteHP": "acute_left",
    "RightAcuteHP": "acute_right",
    "LeftHP": "hp_left",
    "RightHP": "hp_right",
    "LeftOpenHP": "open_hp_left",
    "RightOpenHP": "open_hp_right",

    # Square corners
    "LeftSquare": "square_left",
    "RightSquare": "square_right",

    # Sudden corners
    "SuddenLeft": "",
    "SuddenRight": "",

    # Chicanes
    "LeftChicane": "",
    "RightChicane": "",
    "LeftChicaneEntry": "chicane_left_entry",
    "RightChicaneEntry": "chicane_right_entry",
    "Chicane": "chicane",

    # Flat / kink
    "LeftFlat": "flat_left",
    "RightFlat": "flat_right",
    "LeftKink": "",
    "RightKink": "",

    "Kinks": "twisty",
    "KinksStartingLeft": "twisty_from_left",
    "KinksStartingRight": "twisty_from_right",

    # Go / direction
    "GoLeft": "",
    "GoRight": "",
    "GoStraight": "",

    # Distances
    "Dist40": "40",
    "Dist50": "50",
    "Dist60": "60",
    "Dist70": "70",
    "Dist80": "80",
    "Dist90": "90",
    "Dist100": "100",
    "Dist130": "120",
    "Dist150": "150",
    "Dist170": "160",
    "Dist200": "200",
    "Dist250": "250",
    "Dist300": "300",
    "Dist350": "350",
    "Dist400": "400",

    # Straights / transitions
    "LongStraight": "",
    "VeryLongStraight": "",

    "Over": "over",
    "And": "and",
    "Into": "into",
    "After": "after",

    # Caution / cuts
    "Caution": "caution",
    "DontCut": "dont_cut",
    "Dont": "dont",
    "Cut": "cut",
    "SmallCut": "small_cut",
    "BigCut": "",
    "Yes": "",
    "CutIn": "",

    # Visibility
    "Hidden": "unseen",
    "Blind": "blind",

    # Braking
    "Brake": "brake",
    "HeavyBrake": "",
    "Handbrake": "handbrake",

    # Road camber
    "BadCamber": "badcamber",

    # Flat out
    "FlatOut": "",
    "Slippery": "slippy",

    # Keep line
    "KeepLeft": "keep_left",
    "KeepRight": "keep_right",
    "KeepMiddle": "keep_middle",
    "KeepIn": "keep_in",
    "KeepOut": "keep_out",

    # Warnings
    "CautionInside": "",
    "CautionOutside": "",

    "Sudden": "sudden",
    "Immediate": "immediate",

    # Timing
    "TightensLate": "tightens_late",
    "OpensLate": "opens_late",
    "Late": "late",
    "Early": "early",

    # Speed modifiers
    "SlowDown": "slow",
    "Long": "long",
    "VeryLong": "verylong",
    "Short": "short",
    "ShortMale": "short",
    "LongMale": "short",

    # Corner behavior
    "Tightens": "tightens",
    "Opens": "opens",
    "Narrows": "narrows",
    "NarrowsOutside": "",
    "NarrowsInside": "",
    "NarrowsLeft": "",
    "NarrowsRight": "",
    "Widens": "widens",
    "WidensOutside": "",
    "WidensInside": "",
    "WidensLeft": "",
    "WidensRight": "",

    # Progressive tightening
    "Tighten1": "tightens_one",
    "Tighten2": "tightens_two",
    "Tighten3": "tightens_three",
    "Tighten4": "tightens_four",
    "Tighten5": "tightens_five",

    # Crests
    "SmallCrest": "small_crest",
    "BigCrest": "",
    "Crest": "crest",
    "OverCrest": "over_crest",
    "FlatCrest": "flat_crest",

    # Jumps
    "JumpMaybe": "jump_maybe",
    "JumpSmall": "small_jump",
    "OverJumpSmall": "over_small_jump",
    "JumpBig": "big_jump",
    "OverBigJump": "over_big_jump",
    "Jump": "jump",
    "OverJump": "over_jump",

    # Holes
    "Hole": "hole",
    "Plus": "plus",
    "Minus": "minus",
    "Holes": "",

    # Lines
    "Inside": "inside",
    "Outside": "outside",

    # Bumps
    "Bump": "bump",
    "OverBump": "",
    "Bumps": "bumps",
    "OverBumps": "",

    # Dips
    "Dip": "dip",
    "IntoDip": "",
    "BigDip": "",

    # Water
    "Ford": "ford",

    # Ditches
    "Ditch": "ditch",
    "DitchInside": "ditch_in",
    "DitchOutside": "ditch_out",

    # Surfaces
    "Rough": "rough",
    "Loose": "",
    "Gravel": "gravel",
    "OnGravel": "on_gravel",
    "Asphalt": "",
    "OnAsphalt": "on_tarmac",
    "Snow": "snow",
    "OnSnow": "on_snow",
    "Ice": "ice",
    "OnIce": "",
    "SnowAndIce": "",
    "OnSnowAndIce": "",
    "Concrete": "concrete",
    "OnConcrete": "on_concrete",
    "Pavement": "",
    "OnPavement": "",
    "LoseGravel": "loose_gravel",
    "OnLooseGravel": "",
    "Cobbles": "cobbles",
    "OnCobbles": "",

    # Potholes
    "Pothole1": "",
    "Pothole2": "",
    "Potholes1": "",
    "Potholes2": "",

    # Junctions
    "AtTheHouse": "at_house",
    "AtTheCrossroad": "",
    "Crossroad": "",
    "AfterCrossroad": "",
    "AtJunction": "at_junction",
    "Junction": "junction",
    "AfterJunction": "",

    # Roundabout
    "AtTheRoundabout": "",
    "Roundabout": "roundabout",

    # Logs / trees
    "LogsOutside": "logs_out",
    "LogsInside": "logs_in",
    "Logs": "logs",

    "ThreesOutside": "",
    "ThreesInside": "",
    "Threes": "trees",

    "TreeOutside": "tree_out",
    "TreeInside": "tree_in",
    "Tree": "tree",

    # Bridges
    "OverBridge": "over_bridge",
    "Bridge": "bridge",
    "UnderBridge": "",

    # Gates
    "ThroughGate": "through_gate",
    "Gate": "gate",
    "AtTheGate": "at_gate",

    # Rail / fence
    "AtTheRail": "",

    # Elevation
    "Downhill": "",
    "UpHill": "",
    "Up": "up",
    "Down": "down",

    # Water
    "Water": "water",
    "WaterSplash": "",
    "ThroughWater": "",

    # Tunnel
    "Tunnel": "tunnel",
    "ThroughTunnel": "",

    # Ruts
    "Ruts": "ruts",

    # Obstacles
    "Barrel": "",
    "Tyres": "tires",
    "Pole": "post",
    "Bale": "bale",

    "AroundBarrel": "",
    "AroundTyres": "",
    "AroundPole": "",
    "AroundBale": "",
    "AroundSign": "",
    "AroundSigns": "",

    "AtTheBarrel": "at_barrel",
    "AtTheTyres": "",
    "AtThePoles": "",
    "AtTheBale": "at_bale",
    "AtTheSigns": "",

    "Signs": "",
    "AfterTheSigns": "",
    "AtTheSign": "at_sign",
    "Sign": "sign",
    "AfterTheSign": "",

    # Finish / stop
    "StopAtMarshals": "marshalls",
    "AfterEnd": "",
    "Finish": "finish",

    # Rocks
    "Rock": "rock",
    "Rocks": "rocks",
    "RocksInside": "rocks_in",
    "RocksOutside": "rocks_out",

    # Conditions
    "Wet": "wet",
    "Mud": "muddy"
}


BASE_PATH = "B:\\Koen\\Documents\\Assetto Corsa Rally\\DDF\\"
sound_table = {}

for key, value in conversion.items():
    if value.strip() == "":
        continue

    sound_table[key] = []
    for file in os.listdir(BASE_PATH):
        file_name = re.sub(r"_?\d*\.ogg$", "", file)
        if file_name == value:
            sound_table[key].append(BASE_PATH + file)

for key, value in sound_table.items():
    for i, file in enumerate(value):
        new_name = f"ddf\\{key}_{i + 1}.wav"
        print(new_name)
        os.system(f"ffmpeg -i \"{file}\" \"{new_name}\"")

print("Done.")