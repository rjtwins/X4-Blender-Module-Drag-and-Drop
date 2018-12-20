import xml.etree.ElementTree as ET
from xml.dom.minidom import parse, parseString
from pyquaternion import Quaternion as quat
import naming as name
from glob import glob
import ctypes


#For EXE error handling and questions.
def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

#Read the input and generate connection nodes per read object.
def make_tree(file):
	#parse input xml (x3d)
	tree = ET.parse(file)

	#Generate xml for output
	root = tree.getroot()
	output = ET.Element("root")

	#bool to mirror or not
	mirrorx = True

	#For each node in the input with the tag 'Transform' parse to get the name, location and rotation.
	#Translate rotation to ingame view and construct a connection node for the output.
	#Mirror if requested.
	for node in root.iter('Transform'):
	    id, x, y ,z, rot = parsex3d(node)
	    q = [0,0,0,0]
	    try:
	        q = quat(axis=[float(rot[0]), float(rot[1]), float(rot[2])], angle=float(rot[3]))
	    except ZeroDivisionError:
	        q = [0,0,0,1]

	    q = [q[0]*-1,q[1]*-1,q[3],q[2]*-1]
	    construct(output, id, x, y, z, q)

	    if not mirrorx or "center" in id or not ("left" in id or "right" in id):
	        continue
	    id, x, q = xmirror(id, x, q)
	    construct(output, id, x, y, z, q)
	return output

#Parse a node from the input.
#Read information from relervant atributes and transform the location to ingame view.
def parsex3d(node):
    id = node.get('DEF').replace('_ifs_TRANSFORM','')
    loc = node.get('translation')
    rot = node.get('rotation')
    loc = loc.split()
    rot = rot.split()
    x = float(loc[0]) * -100
    y = float(loc[2]) * 100
    z = float(loc[1]) * -100
    return id, x, y, z, rot

#Construct the connection node for the output.
def construct(output, id, x, y, z, q):
	id = id.split('_')
	try:
		tags = name.tag_dict[id[1]]
		conname = name.name_dict[id[1]]
	except KeyError:
		Mbox("Key Error", "There is something wrong with either your separation, or you are trying to use a module not supported yet."
			"\nNaming convention: groupname_type_nr-in-group"
			"\nExample: left-top-bat-1_lturret_1",0)

	nr = id[2]
	group = id[0]
	id = conname + "_" + id[0] + "-" + id[2]

	connection = ET.SubElement(output, "connection", name=id, group=group, tags=tags)
	offset = ET.SubElement(connection, "offset")
	ET.SubElement(offset, "position", x=str(x), y=str(y), z=str(z))
	ET.SubElement(offset, "quaternion", qx=str(q[1]), qy=str(q[2]), qz=str(q[3]), qw=str(q[0]))

def xmirror(id, x, q):
    #Mirror over x source : https://stackoverflow.com/questions/32438252/efficient-way-to-apply-mirror-effect-on-quaternion-rotation
    x = x * -1
    q = [q[0], q[1],q[2]*-1,q[3]*-1]

    if "left" in id:
        id = id.replace("left", "right")
    else:
        id = id.replace("right", "left")
    return id, x, q

##INIT##
#Find all files with the right extension
files = glob('./*.x3d')
if Mbox("Start", "The following files where detected for input:\n" + "\n".join(files) +"\nDo you want to continue?", 4) == 7:
	exit()

if Mbox("Mirror", "Do you want to mirror left/right?", 4) == 7:
	mirrorx = False

#For each file with the right extension process, make a tree and generate output.
#Store output in file with the origional name + _output.xml 
for file in files:
	output = make_tree(file)
	outputfile = file[2:-4] + "_output.xml"
	tree_string = ET.tostring(output)
	xml = parseString(tree_string)
	pretty_xml_as_string = xml.toprettyxml()
	file = open(outputfile,"w+")
	file.write(pretty_xml_as_string)
	file.close()
Mbox("Done", "", 1)