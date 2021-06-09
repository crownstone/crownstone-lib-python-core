"""
An interface base to define packet formats in short and concise fashion.

Example usage can (for now) be found in CrownstonePacketExample.py
"""
from crownstone_core.packets.PacketFormat import *

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
				customInit(self, args, kwargs)

			# add attributes to the dict for the packetFields and assign
			# default values to them, at least if they weren't constructed in
			# the customInit yet.
			for fieldName, fieldType in packetFields.items():
				if fieldName not in self.__dict__:
					self.__dict__[fieldName] = fieldType.getDefault(parent=self)

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

