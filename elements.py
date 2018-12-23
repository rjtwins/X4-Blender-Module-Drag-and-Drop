import naming as name
import xml.etree.ElementTree as ET
import element

def gen_element(id, location, rotation):
	if id == None:
		return -8
	if location == None or len(location) != 3:
		return -3
	if rotation == None or len(rotation) != 4:
		return -4

	#what are we building ?
	if 'waypoint' in id:
		el = Waypoint(id, location)
	else:
		el = Connection(id, location, rotation)
	result = el.generate()
	return result, el


#Superclass for all elements
class Element:
	location 	= []
	rotation	= []
	con_name	= None
	con_type 	= None
	con_nr 		= None
	element 	= None
	id_full		= None
	id_elements = None

	def __init__(self, id, location, rotation=None):
		self.id = id
		self.location = location
		self.rotation = rotation

	def generate(self):
		self.id_elements = self.id.split('_')
		#There can NEVER be more then 3 elments to a id (group_type_nr) goups are optional so we ar not using them here
		if len(self.id_elements) > 3:
			return -1
		self.con_nr = self.id_elements[-1]
		self.con_type = self.id_elements[-2]
		return 0

	def process(self):
		try:
			self.tags = name.tag_dict[self.con_type]
			self.con_name = name.name_dict[self.con_type]
		except KeyError:
			return -2
		return 0

	def construct(self):
		self.fullname = '%s_%s' % (self.con_name, self.con_nr)
		self.element = ET.Element("connection", name=self.fullname, tags=self.tags)
		ET.SubElement(self.element, "offset")
		ET.SubElement(self.element.find('offset'), "position", x=str(self.location[0]), y=str(self.location[1]), z=str(self.location[2]))
		return 0

	def add_to(self, parent):
		if parent == None or self.element == None:
			return -1
		parent.append(self.element)
		return 0

	#Getters
	def get_element(self):
		return self.element
	def get_fullname(self):
		return self.fullname
		return self.group
	def get_location(self):
		return self.location

class Connection(Element):
	'''Contains a connection in all its forms and flavours.
	This clas is ment to be very transparent to outside observers or interaction as it is inted to be used for other
	things later on in the project.
	Error Handling via return codes
	-1 Incorrect number of elements supplied, try and remove any special characters from your module names (. / @ * ect.)
	-2 Element not supported, or error in element type name
	-3 Incorrect coordinates sceme supplied, either to many or to few.
	-4 Incorrect rotation sceme supplied, either to many or to few.
	'''
	con_group 	= None
	no_rot	 	= False
	is_grouped 	= True
	def __init__(self, id, location, rotation=None):
		super().__init__(id, location, rotation)
		
	def generate(self):
		result = super().generate()
		if result != 0:
			return result
		try:
			self.con_group = self.id_elements[-3]
		except IndexError:
			con_group = False
		result = self.process()
		if result != 0:
			return result

		result = self.construct()
		if result != 0:
			return result
		return 0
		
	def process(self):
		result = super().process()
		if result != 0:
			return result

		if 'engine' in self.con_type:
			self.no_rot = True

		return 0

	def construct(self):
		result = super().construct()
		if result != 0:
			return result

		if self.is_grouped:
			self.fullname = '%s_%s_%s' % (self.con_name, self.con_group, self.con_nr)
			self.element.set('name', self.fullname)
			self.element.set('group', self.con_group)

		if self.no_rot:
			return 0
		ET.SubElement(self.element.find('offset'), "quaternion", qx=str(self.rotation[1]), qy=str(self.rotation[2]), qz=str(self.rotation[3]), qw=str(self.rotation[0]))
		return 0

class Waypoint(Element):
	def test():
		print("test")
