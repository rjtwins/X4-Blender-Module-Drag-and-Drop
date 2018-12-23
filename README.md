# X4-Blender-Module-Drag-and-Drop V4

Python script to enable drag and drop of hard-points in Blender (or any tool that can export to x3d) for X4 foundations.

Egosoft forums: https://forum.egosoft.com/viewtopic.php?f=181&t=409209

X4 Foundations nexus (zip outdated):https://www.nexusmods.com/x4foundations/mods/155/?tab=posts&jump_to_comment=66174131

WARNING: Included EXE will be out of date from time to time, to ensure you have the latest version use the python script.
### How To
<details>
  <summary>Click to expand</summary>
  
  - Convert your XML to DAE (https://forum.egosoft.com/viewtopic.php?f=181&t=404786#p4769763)
  - Open your model in blender and start putting down your "hard-points" the script can mirror (will be queried when script is run) for you so you only need to do one side.
  - Rename hard-points according to the naming scheme so the script can recognize what you are putting down.
  - Select all to be exported hard-points (you do not want to select the ship here) and select export to X3D.
  - In the export settings make sure have, y-forward, z-up and only "selection only" selected. If you are not using blender the axis might be different you will need to experiment to find out.
  - Run either gui.py or main.exe an interface will open.
  - Select your input files and set their options as you like (mirror/inject)
  - Press start.
  - If you are injecting you will be asked for each file into what file you want to inject. Injected xml code will be injected after the last ```<connection></connection>``` element in the selected file.
  - If you are just outputting there will be %input%_output.xml files in the script root directory. Copy the content of this file over between ```<connections></connections>```
  - Video tutorial (outdated) https://youtu.be/b8-ie1u05Lw
  
  </details>

### Details on specific Modules and Elements
<details>
  <summary>Click to expand</summary>

#### Generic Elements
  - Generic elements can be placed down to get their location and orientation.
  - They will apear as ```con_generic_generic_nr``` under ```<connections></connections>```

#### Engines:
  - Engines can only face backwards.
  - You can only ever have one engine size on each ship, aka no mixing of L and XL engines.
  - Engines behave weirdly when not in one group together
 
#### Shields:
  - When in a group will only shield components in group and not the ship as a whole.
  - When not in a group will shield ship.

#### Strorage
  - storage and ship storage (for storing fighter/corvette/frigate) modules indicate the location for internal(as far as I can tell invisible) ship and cargo storage. 
  - The connection point they indicate needs to be assgined to a storage component macro in the ship marco.

### Waypoints
  - Waypoints are for "mass trafic" moving (also for docking path of small ships I suspect).
  - There are 4 types of waypoints, waypoints, start dock waypoints, end dock waypoints and close link waypoints.
  - If not injected waypoints are stored in the output file under ```<waypoints></waypoints>```.

### Playercontroll/Cockpits
  - There are several indicators of playercontroll (camera location?), ai movement points, teleporter indicator, cockpit indicator ect.
  - Currently only playercontroll and the cockpit location are supported.
  
#### Docking areas
  - There are two types of docking areas, NOTE: I think these areas do not indicate the location of the docking mesh, rather the location of where the ship lands?
  - Currently (and as far as I can tell all ship to ship docking indicators) the dock xs for masstrafic and dockingarea for other ships are supported.
  - Launchtubes are also supported.

  </details>
  
### Naming Scheme
<details>
  <summary>Click to expand</summary>
  
```
_ is used as separator do not use this outside of as stated below.
Refrain from using special characters like (@!#$%^&*.,), '-' is allowed.

groupname_type_nr-in-group

groupname       Name of the group, optional.
type            Type of the component (see component list)
nr-in-group     Nr. of component in group.

options:
include 'left' or 'right' in your group name if you want the group to be mirrored.

Examples:
left-top-bat-1_lturret_2
lshield_1
medium-group-center_lshield_1
funcannongroup-1_mturret_666
```
</details>

### Supported Modules
<details>
  <summary>Click to expand</summary>
  
```
Supported modules (m indicates missile capable turret)
#Generic
"generic"
 
#Turrets 
"lturret"
 "lmturret"
"mturret"
"mmturret"
"sturret"
"smturret"
#Shields

"xlshield"
"lshield"
"mshield"
"sshield"
#Engines
"xlengine"
"lengine"
"mengine"
"sengine"
#Countermeasures
"counter"
#Fixed weapons 
"lweap"
"mweap"
"sweap"
"lmweap"
"mmweap"
"smweap"
#Waypoints
"stawaypoint"
"endwaypoint"
"waypoint"
"clowaypoint"
#Player controll/cockpit
"playerctrl"
"cockpit":
#Storage modules
"storage" :
"shipstorage"
#Docking
"dock_xs"
"dockarea"
"launchtube"
```
</details>

### Requirements
<details>
  <summary>Click to expand</summary>
  For exe users
  
    - none
  
  For python users
  
    - Python 3.7 https://www.python.org/
    - pyquaternion http://kieranwynn.github.io/pyquaternion/
    
</details>

### Currently working on:
  - Proper docking
  - More player and AI controll elements (aka cockpit locations, betty sound origion ect.).
  - XML and XMF intergration (long term goal).
