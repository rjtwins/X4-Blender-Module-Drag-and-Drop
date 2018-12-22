# X4-Blender-Module-Drag-and-Drop

Python script to enable drag and drop of hard-points in Blender (or any tool that can export to x3d) for X4 foundations.
Egosoft forums: https://forum.egosoft.com/viewtopic.php?f=181&t=409209
X4 Foundations nexus (zip outdated):https://www.nexusmods.com/x4foundations/mods/155/?tab=posts&jump_to_comment=66174131
### How To
<details>
  <summary>Click to expand</summary>
  
  - Convert your XML to DAE (https://forum.egosoft.com/viewtopic.php?f=181&t=404786#p4769763)
  - Open your model in blender and start putting down your "hard-points" the script can mirror (will be querried when script is run) for you so you only need to do one side.
  - Rename hard-points according to the naming scheme so the script can recognize what you are putting down.
  - Select all to be exported hard-points (you do not want to select the ship here) and select export to X3D.
  - In the export settings make sure have, y-forward, z-up and only "selection only" selected. If you are not using blender the axis might be different you will need to experiment to find out.
  - Run either gui.py or main.exe an interface will open.
  - Select your input files and set their options as you like (mirror/inject)
  - Press start.
  - If you are injecting you will be asked for each file into what file you want to inject. Injected xml code will be injected afther the last <connection></connection> elelment in the selected file.
  - If you are just outputting there will be %input%_output.xml files in the scipt root directory. Copy the content of this file over between ```<connections></connections>```
  
  </details>

### Limitation
<details>
  <summary>Click to expand</summary>
  
#### Engines:
  - Engines can only face backwards.
  - You can only ever have one engine size on each ship, aka no mixing of L and XL engines.
  - Engines behave weirdly when not in one group together
 
#### Shields:

  - When in a group will only shield comonents in group and not the ship as a whole.
  - When not in a group will shield ship.
  
  </details>
  
### Naming Sceme
<details>
  <summary>Click to expand</summary>
  
```
_ is used as separator do not use this outside of as stated below.
Refrain from using sepcial characters like (@!#$%^&*.,) '-' is allowed.

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

### Suported Modules
<details>
  <summary>Click to expand</summary>
  
```
Supported modules (m indicates missile capable turret)
lturret
lmturret	
mturret
mmturret
sturret
ssturret
xlshield
lshield
mshield
sshield
xlengine
lengine
mengine
sengine
counter (countermeasures)
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
