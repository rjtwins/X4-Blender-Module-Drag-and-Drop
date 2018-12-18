import xml.etree.ElementTree as ET
from xml.dom.minidom import parse, parseString
from math import cos, sin, tan, radians

#stolen from http://www.euclideanspace.com/maths/geometry/rotations/conversions/eulerToQuaternion/index.htm:
def quaternion(yaw, pitch, roll):
    #Assuming the angles are in radians.
    c1 = cos(yaw/2)
    s1 = sin(yaw/2)
    c2 = cos(pitch/2)
    s2 = sin(pitch/2)
    c3 = cos(roll/2)
    s3 = sin(roll/2)
    c1c2 = c1*c2
    s1s2 = s1*s2
    w =c1c2*c3 - s1s2*s3
    x =c1c2*s3 + s1s2*c3
    y =s1*c2*c3 + c1*s2*s3
    z =c1*s2*c3 - s1*c2*s3
    return [w, x, y ,z]

def constructr(temp_root, id, x, y, z, yaw, pitch, roll):
    id = "con_turret_laser_l_" + id
    nr = id.find("_bat_")
    groupnr = id[nr + 5]
    grouploc = ""
    if "left" in id:
        grouploc = "left"
    elif "right" in id:
        grouploc = "right"
    elif "center" in id:
        grouploc = "center"
    if "down" in id:
        grouploc = grouploc + "_down"
    elif "top" in id:
        grouploc = grouploc + "_top"
    if "side" in id:
        grouploc = grouploc + "_side"
    group = grouploc + "_bat_" + groupnr
    connection = ET.SubElement(temp_root, "connection", name=id, group=group, tags="turret large standard ")
    offset = ET.SubElement(connection, "offset")
    ET.SubElement(offset, "position", x=str(x), y=str(y), z=str(z))
    ET.SubElement(offset, "rotation", yaw=str(yaw), pitch=str(pitch), roll=str(roll))

def constructq(temp_root, id, x, y, z, q):
    id = "con_turret_laser_l_" + id
    nr = id.find("_bat_")
    groupnr = id[nr + 5]
    grouploc = ""
    if "left" in id:
        grouploc = "left"
    elif "right" in id:
        grouploc = "right"
    elif "center" in id:
        grouploc = "center"
    if "down" in id:
        grouploc = grouploc + "_down"
    elif "top" in id:
        grouploc = grouploc + "_top"
    if "side" in id:
        grouploc = grouploc + "_side"
    group = grouploc + "_bat_" + groupnr
    connection = ET.SubElement(temp_root, "connection", name=id, group=group, tags="turret large standard ")
    offset = ET.SubElement(connection, "offset")
    ET.SubElement(offset, "position", x=str(x), y=str(y), z=str(z))
    ET.SubElement(offset, "quaternion", qx=str(q[1]), qy=str(q[2]), qz=str(q[3]), qw=str(q[0]))


tree = ET.parse('input.dae')
root = tree.getroot()
outputr = ET.Element("root")
outputq = ET.Element("root")
#bool to mirror or not
mx = False

for node in root.iter('{http://www.collada.org/2005/11/COLLADASchema}node'):
    id = node.get('id')
    loc = node[0].text.split()
    #Going from a left handed z up sytem to a right handed y up
    x = float(loc[0]) * -100
    z = float(loc[1]) * -100
    y = float(loc[2]) * 100
    yaw = float(node[1].text.split()[3])
    roll = float(node[2].text.split()[3])
    pitch = float(node[3].text.split()[3])

    #make a quanternion
    q = quaternion(radians(yaw), radians(pitch), radians(roll))

    #Convert rotation to game system
    #https://stackoverflow.com/questions/28673777/convert-quaternion-from-right-handed-to-left-handed-coordinate-system
    q = [q[0],q[1]*-1,q[3]*-1,q[2]*-1]

    yaw = yaw * -1 
    if "top" in id:
        pitch = pitch * -1
    
    constructq(outputq, id, x, y, z, q)
    constructr(outputr, id, x, y, z, yaw, pitch, roll)

    #TODO Mirror over x axis
    # if mx and not "center" in id:
    #     if "left" in id:
    #         id = id.replace("left", "right")
    #     else:
    #         id = id.replace("right", "left")
    #     x = -1 * x
    #     # yaw = yaw * -1
    #     # roll = roll * -1
    #     # https://stackoverflow.com/questions/32438252/efficient-way-to-apply-mirror-effect-on-quaternion-rotation
    #     q=[q[0],q[1],q[2]*-1,q[3]*-1]
    #     constructq(new_root, id, x, y, z, q)

#Output both methods for debugging
tree_string = ET.tostring(outputr)
xml = parseString(tree_string)
pretty_xml_as_string = xml.toprettyxml()
print(pretty_xml_as_string)
file = open("outputr.xml","w+")
file.write(pretty_xml_as_string)
file.close()

tree_string = ET.tostring(outputq)
xml = parseString(tree_string)
pretty_xml_as_string = xml.toprettyxml()
print(pretty_xml_as_string)
file = open("outputq.xml","w+")
file.write(pretty_xml_as_string)
file.close()