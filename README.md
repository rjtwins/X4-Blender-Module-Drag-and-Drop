# X4-Blender-Module-Drag-and-Drop
Python script to enable drag and drop of hard-points in Blender (or any tool that can export to x3d).
To be clear here, this is NOT a tool that allows you to modify ships and import them. Just their surface hard-points.
If you want to import/export ships I suggest you goto: https://forum.egosoft.com/viewtopic.php?f=181&t=404786#p4769763 
or search the forums as there are several topics on this. 

Also keep an eye on the version sinse its still regularly updated.

[spoiler title=For python script users]The script is written in python 3.7 so you will need a python installation :

https://www.python.org/

As well as the pyquaternion module.

If you have no idea what I'm talking about here I suggest you use the EXE instead.
[/spoiler]

[url=https://www.youtube.com/watch?v=b8-ie1u05Lw] Short video tutorial [/url] (OUTDATED)

How this works
-Convert your XML to DAE (https://forum.egosoft.com/viewtopic.php?f=181&t=404786#p4769763)
-Open your model in blender and start putting down your "hard-points" the script can mirror (well be querried when script is run) for you so you only need to do one side.
NOTE: There are templates for supported modules in the scripts root/templates, all combined in a BLEND file and each individually in DAE files.
-READ THE NAMING SCHEME!
-Rename hard-points according to the naming scheme so the script can recognize what you are putting down.
-Select all to be exported hard-points (you do not want to select the ship here) and export to X3D with the right settings to the root directory of where the script is located.
[spoiler title=settings][img]https://i.imgur.com/AIUPWcT.png[/img][/spoiler] 
NOTE: If you are not using Blender the upward and forward axis might be different, you will have to experiment to find out what is what by trial and error.
-Run gui.py or main.exe, an interface will open up where you can choose what files, if you want to mirror and or inject into an existing ship file.
-If needed open the output files with a text editor and copy over the connections into your ship file (assets/units/size_xx/ship_file.xml between <connections> </connections>.

[spoiler title=Using Engines and Shields]
Engines:
Engines can only look directly backward and will show in odd angles if given angular information.
Therefore whatever angle you place the hardpoint at, engines will always be translated to having no pitch/yaw/roll and look directly behind.
You can only have ONE size of engines on your ship  :cry: , if you put more then one size things will start to behave weirdly in game.

Shields:
Shields can either be in no group (by including the nogroup group name), in which case they provide shielding for the ship. Or in a group in which case they provide
shielding for the group ONLY. So if you have only shield in a group they will still only shield each other and not the ship.
[/spoiler]

[spoiler title=naming scheme][code]Naming scheme:
NOTE: _ is used as separator do not use this outside of as stated below.

groupname_type_nr-in-group

groupname				Can be anything if it contains 'nogroup' no group will be assigned. 
					This MUST be done for ship wide shields otherwise the shield will shield the components in the group only.
type					Type of component (see list below for possibilities)
nr					Nr. of component in group.

options:
include 'left' or 'right' in your group name if you want the group to be mirrored.

Examples:
left-top-bat-1_lturret_2
let-nogroup_lshield_1
funcannongroup-1_mturret_666
[/code][/spoiler]
[spoiler title=supported modules][code]
In these the m in lmturret indicates it can fire missiles.

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
[/code][/spoiler]

[spoiler title=old post]First off, if a method of doing this already exists, please relief me from my suffering.

Now, I've been working on little python script where you can simply drag and drop modules on an "object" into Blender (using blenders many amazing functionalities), 
run a script and boom connection point schema to copy paste into your ship XML.

https://github.com/rjtwins/dea-turret-translator

How this works
-Convert your XML to DAE (https://forum.egosoft.com/viewtopic.php?f=181&t=404786#p4769763)
-Open your model in blender and start putting down your "modules" the script will mirror for you (turned off atm) so you only need to do one side.
-Rename modules according to the naming scheme so the script can recognize what you are putting down (turrets only for now but all modules are possible).
-Select all to be exported modules and export to DAE with the right settings (Selection Only, Transformation type: TransRotLoc)
[spoiler][img]https://i.imgur.com/zIQ9KDv.png[/img][/spoiler]
[spoiler][img]https://i.imgur.com/GBMYj5F.png[/img][/spoiler]

Now here is where I run into some trouble, this works just fine, as long as the module you are putting down is not facing too much towards the origins of x and y (aka forward) If that happens an effect known as gimble lock occurs. To fix this you can store the rotation in another format, like quaternion, however, I've not been able to get this
working so far. The rotation is way off and inconsistent when converting to a quaternion. Is there perhaps a better method?[/spoiler]
