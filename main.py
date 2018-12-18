import xml.etree.ElementTree as ET
from xml.dom.minidom import parse, parseString
from pyquaternion import Quaternion as quat
import naming as name

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

def construct(temp_root, id, x, y, z, q):
    id = id.split('_')
    tags = name.tag_dict[id[1]]
    conname = name.name_dict[id[1]]
    nr = id[2]
    group = id[0]
    id = conname + "_" + id[0] + "-" + id[2]

    connection = ET.SubElement(temp_root, "connection", name=id, group=group, tags=tags)
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

tree = ET.parse('input.x3d')
root = tree.getroot()
outputr = ET.Element("root")
outputq = ET.Element("root")

#bool to mirror or not
mirrorx = True

for node in root.iter('Transform'):
    id, x, y ,z, rot = parsex3d(node)

    q = quat(axis=[float(rot[0]), float(rot[1]), float(rot[2])], angle=float(rot[3]))

    #The inversing MUST be conditional to where the part is, keep a lookout for this
    q = [q[0]*-1,q[1]*-1,q[3],q[2]*-1]

    construct(outputq, id, x, y, z, q)

    if not mirrorx or "center" in id:
        continue
    id, x, q = xmirror(id, x, q)
    construct(outputq, id, x, y, z, q)


#Output for debugging
tree_string = ET.tostring(outputq)
xml = parseString(tree_string)
pretty_xml_as_string = xml.toprettyxml()
print(pretty_xml_as_string)
file = open("output.xml","w+")
file.write(pretty_xml_as_string)
file.close()