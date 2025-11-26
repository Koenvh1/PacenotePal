AC Rally Pacenote Pal
=====================

Pacenote Pal is an application for Assetto Corsa Rally that replaces the in-game codriver with an external one.
This way you can use custom voices, edit the pacenotes per stage, and change the timing.

A demo can be found here: https://youtu.be/Quq5dFNgtvQ

**This software is nowhere near finished** and has many rough edges.

How it works
------------

1. Set the audio for the in-game spotter to 0%
2. Start the program
3. Select your stage
4. Press start 
5. Drive to the start of the stage. As the countdown starts, press the space bar. You will hear a beep

Adding a voice can be done by adding a folder in the folder `voices`. Changing the pacenotes can be done by 
editing the YAML files in the `pacenotes` folder, or adding a new file.

Changing settings
-----------------

All settings can be found in the `config.yml` file. You can change them by right-clicking on the file and
selecting "Edit in Notepad". Changes only come into effect after restarting the application.

Using your handbrake as start button
------------------------------------

By default, the space bar is used at the start of the stage. This can also be replaced with your handbrake.
To set this up, execute HandbrakeHelper.exe and follow the steps to generate a config for your config.yml.
Once this is set up, engaging the handbrake for at least 70% for two seconds will also trigger the start 
of the stage.

Creating your own pacenotes from scratch
----------------------------------------

Create an empty YAML file for your pacenotes in the `pacenotes` folder, e.g. `My Notes.yml`. 
Add a single empty pacenote to it and save the file, i.e.:
```
- distance: 0
  link_to_next: false
  notes: []
```
When you (re)start Pacenote Pal, you should see the file in the list. Select it and press start.
Now you can start the stage as normal and start making your pacenotes.

A pacenote consists of three things:
1. `distance` - This is the distance into the stage for this pacenote in metres. Press the "Distance" button to
show the current distance. The codriver will call out this pacenote some time before the pacenote, so you do not 
have to keep that into account.
2. `link_to_next` - Whether when the notes from the current pacenote are called out, the next one will be called 
out immediately after it as well. 
3. `notes` - A list of the audio files to call out at this pacenote. The notes are the audio files from the voices
folder, and you can also add your own audio files if you want notes that are not in the game (e.g. sumppu). If the
file does not exist it will be skipped. The audio files have to be .wav. Additionally, you can add fixed pauses by
adding `PauseX.Ys`, e.g. `Pause1.5s` to pause for 1.5 seconds.

Creating your own voices
------------------------
Create a folder in the folder `voices`. The name of the folder will be the name of your voice. Add all the .wav
files for the notes. The default list the game uses is:

After, AfterCrossroad, AfterEnd, AfterJunction, AfterTheSign, AfterTheSigns, And, AroundBale, AroundBarrel, 
AroundPole, AroundSign, AroundSigns, AroundTyres, Asphalt, AtJunction, AtTheBale, AtTheBarrel, AtTheCrossroad, 
AtTheGate, AtTheHouse, AtThePoles, AtTheRail, AtTheRoundabout, AtTheSign, AtTheSigns, AtTheTyres, BadCamber, 
Bale, Barrel, BigCrest, BigCut, BigDip, Blind, Brake, Bridge, Bump, Bumps, Caution, CautionInside, CautionOutside, 
Chicane, Cobbles, Concrete, Crest, Crossroad, Cut, CutIn, Dip, Dist100, Dist130, Dist150, Dist170, Dist200, 
Dist250, Dist300, Dist350, Dist40, Dist400, Dist50, Dist60, Dist70, Dist80, Dist90, Ditch, DitchInside, 
DitchOutside, Dont, DontCut, Down, Downhill, Early, Finish, FlatCrest, FlatOut, Ford, Gate, GoLeft, GoRight, 
GoStraight, Gravel, Handbrake, HeavyBrake, Hidden, Hole, Holes, Ice, Immediate, Inside, Into, IntoDip, Jump, 
JumpBig, JumpMaybe, JumpSmall, Junction, KeepIn, KeepLeft, KeepMiddle, KeepOut, KeepRight, Kinks, KinksStartingLeft, 
KinksStartingRight, Late, Left1, Left2, Left3, Left4, Left5, Left6, LeftAcuteHP, LeftChicane, LeftChicaneEntry, 
LeftFlat, LeftHP, LeftKink, LeftOpenHP, LeftRight, LeftSquare, Logs, LogsInside, LogsOutside, Long, LongMale, 
LongStraight, Loose, LoseGravel, Minus, Mud, Narrows, NarrowsInside, NarrowsLeft, NarrowsOutside, NarrowsRight, 
OnAsphalt, OnCobbles, OnConcrete, OnGravel, OnIce, OnLooseGravel, OnPavement, OnSnow, OnSnowAndIce, Opens, 
OpensLate, Outside, Over, OverBigJump, OverBridge, OverBump, OverBumps, OverCrest, OverJump, OverJumpSmall, 
Pavement, Plus, Pole, Pothole1, Pothole2, Potholes1, Potholes2, Right1, Right2, Right3, Right4, Right5, Right6, 
RightAcuteHP, RightChicane, RightChicaneEntry, RightFlat, RightHP, RightKink, RightLeft, RightOpenHP, RightSquare, 
Rock, Rocks, RocksInside, RocksOutside, Rough, Roundabout, Ruts, Short, ShortMale, Sign, Signs, Slippery, SlowDown, 
SmallCrest, SmallCut, Snow, SnowAndIce, StopAtMarshals, Sudden, SuddenLeft, SuddenRight, Threes, ThreesInside, 
ThreesOutside, ThroughGate, ThroughTunnel, ThroughWater, Tighten1, Tighten2, Tighten3, Tighten4, Tighten5, Tightens, 
TightensLate, Tree, TreeInside, TreeOutside, Tunnel, Tyres, UnderBridge, Up, UpHill, VeryLong, VeryLongStraight, 
Water, WaterSplash, Wet, Widens, WidensInside, WidensLeft, WidensOutside, WidensRight, Yes

I'm aware there are typos in that list (e.g. ThreesOutside), but that matches what ACR uses internally as 
well. If a file is missing, it will be skipped. It is also possible to add multiple variants of a note by doing
e.g. `After.wav`, `After_1.wav`, `After_2.wav`. It will randomly pick one of the options.

ACR uses 6 for the widest turn and 1 for the tightest turn. Depending on the voice you could make the audio for
Left6 sound like "1 Left", "Fast Left", or something else instead.

Thanks to
---------
- pyaccsharedmemory.py is based on https://github.com/rrennoir/PyAccSharedMemory