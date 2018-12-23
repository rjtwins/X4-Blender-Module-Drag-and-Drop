import xml.etree.ElementTree as ET
from xml.dom.minidom import parse, parseString
from pyquaternion import Quaternion as quat
from glob import glob
import ctypes
from tkinter import filedialog, Tk, messagebox
import elements as elements
import naming as dicts


# Error Handling via return codes
# -1 Incorrect number of elements supplied, try and remove any special characters from your module names (. / @ * ect.)
# -2 Element not supported, or error in element type name
# -3 Incorrect coordinates sceme supplied, either to many or to few.
# -4 Incorrect rotation sceme supplied, either to many or to few.
# -5 File we are tyring to inject to not found or no file selected.


#As I kept adding stuff to this it became uglier and uglier, but still I hope whoever reads this can enjoy the spagetti ball in all its glory.
#Need to remain this class for clarity!
class Main():
	file_list = []
	file_selected = []

	#Current output buffer ?dict?
	output = {}

	def __init__(self):
		self.file_list = []
		self.file_selected = []
		self.output = {}
		for elment_type in dicts.element_root_types:
			self.output[elment_type] = ET.Element(elment_type)

	#For EXE error handling and questions.
	def Mbox(self, title, text, style):
		return ctypes.windll.user32.MessageBoxW(0, text, title, style)

	def print_obj_atribs(self):
		print (', '.join("%s: %s" % item for item in vars(self).items()))

	def Error(self, code, file):
		print("Error Code ", code, file)
		error_codes = {
			-1: "Incorrect number of element in component name.",
			-2: "Element type not supported or error in element name.",
			-3: "Error in coordinate sceme.",
			-4: "Incorrect number of rotational components.",
			-5: "Failed to open file selected for injection or file not present.",
			-6:	"The file you selected to inject into could not be parsed.",
			-7: "The file you selected to inject into has no <connections></connections> node.",
			-8: "Supplied object id was None.",
			-9: "Constructed element is None or element trying to add to is None.",
			-99: "Method faied to return or returned None."

		}
		error = error_codes.get(code, "Error code not documented")
		self.Mbox("ERROR", "Error Code %s\n%s in file %s" % (code, error, file), 1)

	#For injecting, we are connecting the parrent of the existing xml here.
	def make_tree(file, mirror, output_file):
		target = ET.parse(output_file)
		target_root = target.getroot()
		for key in self.output.keys():
			target_parent = root.find('//%s' % str(key))
			output[str(key)] = target_parent
		return self.make_tree(file, mirror)
	
	#Making tree from x3d 
	def make_tree(self, file, mirror):
		#parse input xml (x3d)
		tree = ET.parse(file)
		root = tree.getroot()
		
		#For each node in the input with the tag 'Transform' parse to get the name, location and rotation.
		#Translate rotation to ingame view and construct a connection node for the output.
		#Mirror if requested.
		for node in root.iter('Transform'):
			id, x, y ,z, rot = self.parsex3d(node)
			q = [0,0,0,0]
			try:
			    q = quat(axis=[float(rot[0]), float(rot[1]), float(rot[2])], angle=float(rot[3]))
			except ZeroDivisionError:
			    q = [1,0,0,0]

			q = [q[0]*-1,q[1]*-1,q[3],q[2]*-1]
			#Create an X4 element object and connect it to the right output.
			elements.add_element(id, [x,y,z], q, self.output)

			if not mirror:
				continue

			if not 'left' in id and not 'right' in id:
				continue

			#Mirror
			id, x, q = self.xmirror(id, x, q)

			result = elements.add_element(id, [x,y,z], q, self.output)


	def string_output(self):
		combined_xml_string = ""
		for key in self.output.keys():
			header = str(key)
			xml_string = ET.tostring(self.output[key])
			xml_string = parseString(xml_string)
			xml_string = xml_string.toprettyxml()
			combined_xml_string = "%s%s\n%s" % (combined_xml_string, header, xml_string)
		return combined_xml_string

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
		self.file_list = []
		read_files = filedialog.askopenfilenames(title='Choose a file',filetypes=[("X3D Files", ".x3d")])

		if len(read_files) == 0:
			read_files = []

		for file in read_files:
			self.file_list.append([file,[False,False]])

	def process(self):
		#For each file with the right extension process, make a tree and generate output.
		#Store output in file with the origional name + _output.xml 
		for file_obj in self.file_list:
			file = file_obj[0]
			mirror = file_obj[1][0]
			inject = file_obj[1][1]
			if inject:
				output_file = filedialog.askopenfilename(title = "Select where to inject " + file,filetypes = [("XML Files", ".xml")])
				self.make_tree(file, mirror, output_file)
			else:
				self.make_tree(file, mirror)
				file = file[2:-4]
				file = file + "_output.xml"
			xml = self.string_output()
			print("%s output: \n%s" % (file, xml))
			file = open(file,"w+")
			file.write(xml)
			file.close()
		self.Mbox("Done","",1)