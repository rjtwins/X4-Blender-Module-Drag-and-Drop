import xml.etree.ElementTree as ET
from xml.dom.minidom import parse, parseString
from pyquaternion import Quaternion as quat
import naming as name
from glob import glob
import ctypes
from tkinter import filedialog, Tk, messagebox

#As I kept adding stuff to this it became uglier and uglier, but still I hope whoever reads this can enjoy the spagetti ball in all its glory.
class Main():
	root = Tk()
	root.withdraw()
	file_list = []
	file_selected = []

	#For EXE error handling and questions.
	def Mbox(self, title, text, style):
		return ctypes.windll.user32.MessageBoxW(0, text, title, style)

	def outputdialog(self, file, raw_xml):
		xml = None
		try:
			file = filedialog.askopenfilename(title = "Select where to inject " + file,filetypes = [("XML Files", ".xml")])
			xml = self.override_xml(file, raw_xml)
		except FileNotFoundError:
			self.Mbox("ERROR", "File not found or no file selected.",1)
			
		return file, xml

	#ow boy here we go
	def override_xml(self, file, new_connections):
		#tidy up new_connections cause ITS A MESS
		new_connections = ET.tostring(new_connections)
		new_connections = parseString(new_connections)
		new_connections = new_connections.toprettyxml()
		new_connections = ET.fromstring(new_connections)
		xml = ""
		try:
			xml = ET.parse(file)
		except ET.ParseError:
			self.Mbox("ERROR",file + " could not be parsed and will be skipped.",1)
			return xml

		root = xml.getroot()
		connections = root.find('component/connections')
		try:
			for child in new_connections:
				connections.append(child)
		except AttributeError:
			self.Mbox("Error", "The file you selected to replace in,\n" + file + "\n has no <connections></connections> node.",1)
			return ""

		xml = ET.tostring(root)
		xml = parseString(xml)
		xml = xml.toxml()
		return xml

	#Read the input and generate connection nodes per read object.
	def make_tree(self, file, mirror):
		#parse input xml (x3d)
		tree = ET.parse(file)
		root = tree.getroot()

		#Generate xml for output
		output = ET.Element("root")

		#bool to mirror or not
		mirrorx = True

		#For each node in the input with the tag 'Transform' parse to get the name, location and rotation.
		#Translate rotation to ingame view and construct a connection node for the output.
		#Mirror if requested.
		for node in root.iter('Transform'):
		    id, x, y ,z, rot = self.parsex3d(node)
		    q = [0,0,0,0]
		    try:
		        q = quat(axis=[float(rot[0]), float(rot[1]), float(rot[2])], angle=float(rot[3]))
		    except ZeroDivisionError:
		        q = [0,0,0,1]

		    q = [q[0]*-1,q[1]*-1,q[3],q[2]*-1]
		    self.construct(output, id, x, y, z, q)

		    if not mirror or not mirrorx or "center" in id or not ("left" in id or "right" in id):
		        continue
		    id, x, q = self.xmirror(id, x, q)
		    self.construct(output, id, x, y, z, q)
		return output

	#Parse a node from the input.
	#Read information from relervant atributes and transform the location to ingame view.
	def parsex3d(self, node):
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
	def construct(self, output, id, x, y, z, q):
		id = id.split('_')
		tags = ""
		conname = ""
		try:
			tags = name.tag_dict[id[1]]
			conname = name.name_dict[id[1]]
		except KeyError:
			self.Mbox("Key Error", "There is something wrong with either your separation, or you are trying to use a module not supported yet."
				"\nNaming convention: groupname_type_nr-in-group"
				"\nExample: left-top-bat-1_lturret_1",0)

		nr = id[2]
		group = id[0]

		#Ships shield (shield for overal ship protection) need to NOT be in a group to count towards overal shiels.
		if "nogroup" in group:
			id = conname + "_" + id[0] + "-" + id[2]
			connection = ET.SubElement(output, "connection", name=id, tags=tags)
		else:
			id = conname + "_" + id[0] + "-" + id[2]
			connection = ET.SubElement(output, "connection", name=id, group=group, tags=tags)
		offset = ET.SubElement(connection, "offset")
		ET.SubElement(offset, "position", x=str(x), y=str(y), z=str(z))
		ET.SubElement(offset, "quaternion", qx=str(q[1]), qy=str(q[2]), qz=str(q[3]), qw=str(q[0]))

	def xmirror(self, id, x, q):
	    #Mirror over x source : https://stackoverflow.com/questions/32438252/efficient-way-to-apply-mirror-effect-on-quaternion-rotation
	    x = x * -1
	    q = [q[0], q[1],q[2]*-1,q[3]*-1]

	    if "left" in id:
	        id = id.replace("left", "right")
	    else:
	        id = id.replace("right", "left")
	    return id, x, q

	def select_files(self):
		read_files = filedialog.askopenfilenames(parent=self.root,title='Choose a file',filetypes=[("X3D Files", ".x3d")])

		if len(read_files) == 0:
			read_files = []

		for file in read_files:
			self.file_list.append([file,[False,False]])
		return self.file_list

	def process(self):
		#For each file with the right extension process, make a tree and generate output.
		#Store output in file with the origional name + _output.xml 
		for file_obj in self.file_list:
			file = file_obj[0]
			mirror = file_obj[1][0]
			inject = file_obj[1][1]
			output = self.make_tree(file, mirror)
			rxml = ""
			xml = ""
			rfile = ""
			file = file[2:-4]
			file = file + "_output.xml"
			if inject:
				rfile, rxml = self.outputdialog(file, output)
			if not rxml == "":
				xml = rxml
				file = rfile
			else:
				xml = ET.tostring(output)
				xml = parseString(xml)
				xml = xml.toprettyxml()
				xml = xml.replace('</root>', "").replace('<root>', "").replace('<?xml version="1.0" ?>',"")
				xml = xml[2:-2]
			file = open(file,"w+")
			file.write(xml)
			file.close()
		self.Mbox("Done","",1)
