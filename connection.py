import naming as name
import xml.etree.ElementTree as ET

class Connection:
	'''Contains a connection in all its forms and flavours.
	This clas is ment to be very transparent to outside observers or interaction as it is inted to be used for other
	things later on in the project.
	Error Handling via return codes
	-1 Incorrect number of elements supplied, try and remove any special characters from your module names (. / @ * ect.)
	-2 Element not supported, or error in element type name
	-3 Incorrect coordinates sceme supplied, either to many or to few.
	-4 Incorrect rotation sceme supplied, either to many or to few.
	'''
	location 	= []
	rotation	= []
	fullname	= None
	con_type 	= None
	con_name 	= None
	con_nr 		= None
	con_group 	= None
	tags 		= None
	no_rot	 	= False
	is_grouped 	= False
	element 	= None
	id 			= None
	def __init__(self, id, location, rotation=None):
		##print("Connection.init")
		self.id = id
		self.location = location
		self.rotation = rotation
		#print("Connection.init_done")

		
	def generate(self):
		#print("Connection.generate")
		id_elements = self.id.split('_')
		#print(id_elements)
		if len(id_elements) == 2:
			self.con_type = id_elements[0]
			self.con_nr = id_elements[1]
		elif len(id_elements) == 3:
			grouped = True
			self.con_group = id_elements[0]
			self.con_type = id_elements[1]
			self.con_nr = id_elements[2]
		else:
			#Something is wrong
			return -1
		result = self.process()
		if result != 0:
			return result
		result = self.construct()
		if result != 0:
			return result
		#print("Connection.generate_done")
		return 0
		
	#no group construct, and a whole bunch of error handling.
	def process(self):
		#print("Connection.process")
		try:
			self.tags = name.tag_dict[self.con_type]
			self.con_name = name.name_dict[self.con_type]
		except KeyError:
			return -2
		if 'engine' in self.con_type:
			self.is_engine = True
		if len(self.location) != 3:
			return -3
		#If we do not have 4 rotation parameters, and we do not have 0 rotation parameters and are an engine there is something wrong.
		if len(self.rotation) != 4 and not (len(self.rotation) == 0 and self.is_engine ):
			return -4
		#print("Connection.process_done")
		return 0

	def construct(self):
		#print("Connection.construct")
		if self.is_grouped:
			self.fullname = '%s_%s_%s' % (self.con_name, self.con_group, self.con_nr)
			self.element = ET.Element("connection", name=self.fullname, group=self.con_group, tags=self.tags)
		else:
			self.fullname = '%s_%s' % (self.con_name, self.con_nr)
			self.element = ET.Element("connection", name=self.fullname, tags=self.tags)

		offset = ET.SubElement(self.element, "offset")
		ET.SubElement(offset, "position", x=str(self.location[0]), y=str(self.location[1]), z=str(self.location[2]))

		if self.no_rot:
			#print("Connection.construct_done")
			return 0
		ET.SubElement(offset, "quaternion", qx=str(self.rotation[1]), qy=str(self.rotation[2]), qz=str(self.rotation[3]), qw=str(self.rotation[0]))
		#print("Connection.construct_done")
		return 0

	def add_to(self, parent):
		#print("Connection.add_to")
		#TODO More error handling
		if parent == None:
			return -1
		parent.append(self.element)
		return 0
		#print("Connection.add_to_done")


	#Getters
	def get_element(self):
		return self.element
	def get_is_grouped(self):
		return self.is_grouped
	def get_is_engine(self):
		return self.is_engine
	def get_fullname(self):
		return self.fullname
	def get_group(self):
		if not self.is_grouped:
			return None
		return self.group
	def get_location(self):
		return self.location
	def get_rotation(self):
		if self.no_rot:
			return None
		return self.rotation

	#TODO
	#add more getters