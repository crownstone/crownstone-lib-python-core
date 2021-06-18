"""
An interface base to define packet formats in short and concise fashion.

Example usage can (for now) be found in CrownstonePacketExample.py
"""
from crownstone_core.packets.PacketFormat import *

# TODO: rename
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
		if SerializableField not in bases:
			bases += SerializableField,

		# split the attributes in packet field definitions (name -> Packet subclass) and other attributes
		packetFieldTypes = {fieldName : fieldValue for fieldName,fieldValue in attrs.items() if mcs.isPacketField(fieldValue)}
		otherAttributes  = {fieldName : fieldValue for fieldName,fieldValue in attrs.items() if not mcs.isPacketField(fieldValue)}

		subclassAttributes = otherAttributes

		# add a wrapper to __init__ that initializes the objects serializable fields and
		# add the dict defining which fields are to be serialized to the class variables.
		instanceInit = otherAttributes.get("__init__")
		subclassAttributes["__init__"] = mcs.makeInitMethod(packetFieldTypes, instanceInit)
		subclassAttributes["_serializedFields"] = packetFieldTypes

		return super(CrownstonePacket, mcs).__new__(mcs, subclassName, bases, subclassAttributes)

	@staticmethod
	def isPacketField(fieldValue):
		return issubclass(type(fieldValue), SerializableField)

	@staticmethod
	def makeInitMethod(packetFields, customInit = None):
		def initmethod(self, *args, **kwargs):
			if customInit:
				customInit(self, *args, **kwargs)

			# For fields that haven't been constructed by customInit:
			# - check if there's a keyword argument to assign
			# - check if there is a positiional argument to assign
			# - construct a new object from fieldType.getDefault

			args_generator = (x for x in args)
			for fieldName, fieldType in packetFields.items():
				if getattr(self, fieldName, None) is None:
					field = None
					if field is None and kwargs:
						field = kwargs.pop(fieldName, None)
					if field is None and args:
						field = next(args_generator, None)
					if field is None:
						field = fieldType.getDefault(parent=self)
					setattr(self, fieldName, field)

			# anything unused keyword arguments indicates wrongly constructed object.
			if kwargs:
				raise AttributeError(F"{self.__class__} does not contain an attributes for {kwargs}")

			# same for positional arguments.
			if next(args_generator, None) is not None:
				raise AttributeError(F"{self.__class__} too many positional arguments provided")

		return initmethod

