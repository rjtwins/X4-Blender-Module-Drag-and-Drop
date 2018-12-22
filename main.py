import xml.etree.ElementTree as ET
from xml.dom.minidom import parse, parseString
from pyquaternion import Quaternion as quat
from glob import glob
import ctypes
from tkinter import filedialog, Tk, messagebox
import connection as con


# Error Handling via return codes
# -1 Incorrect number of elements supplied, try and remove any special characters from your module names (. / @ * ect.)
# -2 Element not supported, or error in element type name
# -3 Incorrect coordinates sceme supplied, either to many or to few.
# -4 Incorrect rotation sceme supplied, either to many or to few.
# -5 File we are tyring to inject to not found or no file selected.
			# self.Mbox("ERROR", "File not found or no file selected.",1)


#As I kept adding stuff to this it became uglier and uglier, but still I hope whoever reads this can enjoy the spagetti ball in all its glory.
class Main():
	root = Tk()
	root.withdraw()
	file_list = []
	file_selected = []

	#Current output buffer
	output = None

	#For EXE error handling and questions.
	def Mbox(self, title, text, style):
		return ctypes.windll.user32.MessageBoxW(0, text, title, style)

	def Error(self, code, file):
		error_codes = {
			-1: "Incorrect number of element in component name.",
			-2: "Element type not supported or error in element name.",
			-3: "Error in coordinate sceme.",
			-4: "Incorrect number of rotational components.",
			-5: "Failed to open file selected for injection or file not present.",
			-6:	"The file you selected to inject into could not be parsed.",
			-7: "The file you selected to inject into has no <connections></connections> node."
		}
		error = error_codes.get(code, "Error code not documented")
		Mbox("ERROR", "Error Code %s\n%s in file %s" % (code, error, file))

	def outputdialog(self, file, raw_xml):
		xml = None
		try:
			file = filedialog.askopenfilename(title = "Select where to inject " + file,filetypes = [("XML Files", ".xml")])
			result, xml = self.override_xml(file, raw_xml)
		except FileNotFoundError:
			return -5, "", ""
		except ET.ParseError:
			return -6, "", ""
		except AttributeError:
			return -7, "", ""
		return 0, file, xml

	def override_xml(self, file, new_connections):
		#tidy up new_connections cause ITS A MESS
		new_connections = ET.tostring(new_connections)
		new_connections = parseString(new_connections)
		new_connections = new_connections.toprettyxml()
		new_connections = ET.fromstring(new_connections)

		xml = ET.parse(file)
		root = xml.getroot()
		connections = root.find('component/connections')

		for child in new_connections:
			connections.append(child)

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
		self.output = ET.Element("root")

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

		    #Create an X4 component connection object and connect it to the output.
		    connection = con.Connection(id, [x,y,z], q)
		    result = connection.generate()
		    if result != 0:
		    	return result
		    result = connection.add_to(self.output)
		    if result != 0:
		    	return result

		    if not mirror or "center" in id or not ("left" in id or "right" in id):
		        continue

		    #Mirror
		    id, x, q = self.xmirror(id, x, q)

		    connection = con.Connection(id, [x,y,z], q)
		    result = connection.generate()
		    if result != 0:
		    	return result
		    result = connection.add_to(output)
		    if result != 0:
		    	return result
		    return 0

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
			result = self.make_tree(file, mirror)
			if result != 0:
				self.Error(result, file)
				continue
			xml = ""
			file = file[2:-4]
			file = file + "_output.xml"
			result = 0
			if inject:
				result, temp_file, temp_xml = self.outputdialog(file, self.output)
				if result != 0:
					self.Error(result, file)
					continue
				file = temp_file
				xml = temp_xml
			else:
				#Gemerate output and cleanup output string.
				xml = ET.tostring(output)
				xml = parseString(xml)
				xml = xml.toprettyxml()
				xml = xml.replace('</root>', "").replace('<root>', "").replace('<?xml version="1.0" ?>',"")
				xml = xml[2:-2]
			file = open(file,"w+")
			file.write(xml)
			file.close()
		self.Mbox("Done","",1)
		return 0