import naming as name
import xml.etree.ElementTree as ET

def gen_element(id, location, rotation):
	if id == None:
		return -8
	if location == None or len(location) != 3:
		return -3
	if rotation == None or len(rotation) != 4:
		return -4

	#what are we building ?
	if 'waypoint' in id:
		el = Waypoint(id, location, rotation)
	else:
		el = Connection(id, location, rotation)
	result = el.fill()
	return result, el


#Superclass for all elements
class Element:
	#Location in x,y,z
	location 	= []
	#rotation quat in w,x,y,z
	rotation	= []
	#connection name
	con_name	= ""
	#fully constructed name string
	fullname 	= ""
	#connection type (what surface element)
	con_type	= ""
	#how manied number of this element
	con_nr		= ""
	#Tags assgined to this element
	tags 		= ""
	#Element Tree object containing xml of element
	element 	= None
	#What kind of element is this ?
	element_id	= "element"
	#ID string
	id 			= ""
	#Split ID string
	id_elements	= []


	def __init__(self, id, location, rotation=None):
		self.id = id
		self.location = location
		self.rotation = rotation

	def fill(self):
		result = self.generate()
		if result != 0:
			return result
		result = self.process()
		if result != 0:
			return result
		result = self.construct()
		if result != 0:
			return result
		return 0

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
		self.element = ET.Element(self.element_id, name=self.fullname, tags=self.tags)
		ET.SubElement(self.element, "offset")
		ET.SubElement(self.element.find('offset'), "position", x=str(self.location[0]), y=str(self.location[1]), z=str(self.location[2]))
		if all([ v == 0 for v in self.rotation ]):
			return 0
		ET.SubElement(self.element.find('offset'), "quaternion", qx=str(self.rotation[1]), qy=str(self.rotation[2]), qz=str(self.rotation[3]), qw=str(self.rotation[0]))
		return 0

	def add_to(self, parent):
		if parent == None or self.element == None:
			return -9
		parent.append(self.element)
		return 0

	#Getters
	def get_element(self):
		return self.element
	def get_fullname(self):
		return self.fullname
	def get_location(self):
		return self.location

	def print_obj_atribs(self):
		print (', '.join("%s: %s" % item for item in vars(self).items()))

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
	con_group = None
	def __init__(self, id, location, rotation=None):
		super().__init__(id, location, rotation)
		self.element_id = "connection"
		
	def generate(self):
		result = super().generate()
		if result != 0:
			return result
		try:
			self.con_group = self.id_elements[-3]
		except IndexError:
			con_group = None
		return 0
		
	def process(self):
		if 'engine' in self.con_type:
			#TODO CONFIRM CORRECT ROTATION
			self.rotation = [0,0,0,0]
		result = super().process()
		if result != 0:
			return result
		return 0

	def construct(self):
		result = super().construct()
		if result != 0:
			return result
		if self.con_group != None:
			self.fullname = '%s_%s_%s' % (self.con_name, self.con_group, self.con_nr)
			self.element.set('name', self.fullname)
			self.element.set('group', self.con_group)
		return 0

class Waypoint(Element):
	#list of nr of other waypoints this waypoint is connected to.
	links = []
	def __init__(self, id, location, rotation):
		super().__init__(id, location, rotation)
		self.element_id = "waypoint"

	#Waypoint will define links as type-linknr-linknr-linknr_waypointnr so split it up so we don't end up looking for the name for waypoint-1-12 in the dict.
	def generate(self):
		result = super().generate()
		if result != 0:
			return result
		self.links = self.con_type.split('-')
		self.con_type = self.links[0]
		self.links = self.links[1:]
		return 0

	def construct(self):
		self.fullname = '%s_%s' % (self.con_name, self.con_nr)
		self.element = ET.Element(
			self.element_id, 
			name=self.fullname, 
			tags=self.tags, 
			x=str(self.location[0]), 
			y=str(self.location[1]), 
			z=str(self.location[2]),
			qw=str(self.rotation[0]),
			qx=str(self.rotation[1]),
			qy=str(self.rotation[2]),
			qz=str(self.rotation[3])
			)
		ET.SubElement(self.element, "links")
		for link_nr in self.links:
			ET.SubElement(self.element.find("links"), "link", ref="%s%s" % (self.con_name, link_nr))
		return 0
