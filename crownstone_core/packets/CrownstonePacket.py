"""
An interface base to define packet formats in short and concise fashion.

Example usage can (for now) be found in CrownstonePacketExample.py
"""


class Packet:
	"""
	Defines the interface that packets implement. Subclasses need to actually
	do something in these methods.
	"""
	def getPacket(self):
		pass

	def setPacket(self, bytelist):
		pass

	@classmethod
	def getDefault(cls):
		return None


class CrownstonePacket(type):
	"""
	A CrownstonePacket defines a dataformat that complies with the over-the-line protocol,
	used for Bluetooth connections, mesh and UART.

	CrownstonePacket objects automatically inherit from Packet and have generated serialization/deserialization methods
	as well as a generated constructor that ensures that all fields/values are set to a default.

	Design question:
	- enforce types? E.g. fields serialed to `Uint8` must be `int` etc.?
	"""
	def __new__(mcs, subclassName, bases, attrs):
		print(F"CrownstonePacket: {subclassName}")
		print("   b:", bases)
		print("   a:", attrs)
		bases += Packet,

		# split the attributes in packet field definitions (name -> Packet subclass) and other attributes
		packetFieldTypes = {fieldName : fieldValue for fieldName,fieldValue in attrs.items() if mcs.isPacketField(fieldValue)}
		otherAttributes  = {fieldName : fieldValue for fieldName,fieldValue in attrs.items() if not mcs.isPacketField(fieldValue)}

		subclassAttributes = otherAttributes

		superInit = otherAttributes.get("__init__")
		subclassAttributes["__init__"] = mcs.makeInitMethod(packetFieldTypes, superInit)
		subclassAttributes["_packetFieldTypes"] = packetFieldTypes

		print("subclass attributes", subclassAttributes)
		return super(CrownstonePacket, mcs).__new__(mcs, subclassName, bases, subclassAttributes)

	@staticmethod
	def isPacketField(fieldValue):
		return issubclass(type(fieldValue), Packet)

	@staticmethod
	def makeInitMethod(packetFields, superInit = None):
		def initmethod(self, *args, **kwargs):
			print("--- pre call super init --- ")
			if superInit:
				superInit(self, args,kwargs)
			print(" --- post call super init ---")

			# add attributes to the dict for the packetFields and assign
			# default values to them
			for fieldName, fieldType in packetFields.items():
				self.__dict__[fieldName] = fieldType.getDefault()

			# if any positional arguments are set, assign them in order to
			# the fields of this object.
			if args:
				for t in zip(self.__dict__,args):
					self.__dict__[t[0]] = t[1]

			# any keyword arguments that are contained in the dict are assigned
			# otherwise an AttributeError is thrown
			if kwargs:
				for kwargKey, kwargValue in kwargs.items():
					if kwargKey in self.__dict__:
						self.__dict__[kwargKey] = kwargValue
					else:
						raise AttributeError(F"{self.__class__} does not contain an attribute named {kwargKey}")

		return initmethod


# ----- literal types -------



class Bool(Packet):
	pass

class Uint8(Packet):
	pass


class Uint16(Packet):
    pass

class Uint32(Packet):
	pass

class Int8(Packet):
	pass

class Uint8Enum(Packet):
	pass

class Uint16Enum(Packet):
    pass

class PacketArray(Packet):
	pass

class Variant(Packet):
	def __init__(self, **kwargs):
		pass

