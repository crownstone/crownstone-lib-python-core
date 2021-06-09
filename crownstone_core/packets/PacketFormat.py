from enum import IntEnum

from crownstone_core.util.BufferWriter import BufferWriter
from crownstone_core.util.BufferReader import BufferReader

class SerializableField:
	"""
	Defines the interface that packets implement.
	"""
	def __init__(self, *args, **kwargs):
		pass

	def getPacket(self):
		writer = BufferWriter()
		self.writeBytes(self, writer)
		return writer.getBuffer()

	def loadPacket(self, data):
		pass

	def getDefault(self, parent):
		"""
		Default value of a field is allowed to depend on the siblings of the field
		e.g. in order to automatically get the length of a variable size array.
		These can be obtains through a reference of the parent.
		"""
		return None

	def readBytes(self, instance, reader):
		pass

	def writeBytes(self, instance, writer):
		"""
		Generic implementation: loop over all fields in the instance that are supposed to be serialized
		and call writebytes on the respective type.
		"""
		fields = self.__getattribute__("_serializedFields") or dict()
		for fieldName, fieldType in fields.items():
			fieldType.writeBytes(instance.__dict__[fieldName], writer)


# ----- generic integral type -----

class SerializableIntegralField(SerializableField):
	def __init__(self, default=None,  *args, **kwargs):
		super().__init__(*args,**kwargs)
		self.default = kwargs.get("default", default)

	def getDefault(self, parent):
		""" if default is set use that value and transform None into 0 """
		return self.default or 0

# ----- literal types -------

class Bool(SerializableIntegralField):
	def getDefault(self, parent):
		""" if default is set use that value and transform None into False """
		return self.default or False

	def readBytes(self, instance, reader):
		pass

	def writeBytes(self, instance, writer: BufferWriter):
		writer.putUInt8(instance)

# unsigned ints

class Uint8(SerializableIntegralField):
	def readBytes(self, instance, reader):
		pass

	def writeBytes(self, instance, writer: BufferWriter):
		writer.putUInt8(instance)

class Uint16(SerializableIntegralField):
	def readBytes(self, instance, reader):
		pass

	def writeBytes(self, instance, writer: BufferWriter):
		writer.putUInt16(instance)

class Uint32(SerializableIntegralField):
	def readBytes(self, instance, reader):
		pass

	def writeBytes(self, instance, writer: BufferWriter):
		writer.putUInt32(instance)

# signed ints

class Int8(SerializableIntegralField):
	def readBytes(self, instance, reader):
		pass

	def writeBytes(self, instance, writer):
		writer.putInt8(instance)

class Int16(SerializableIntegralField):
	def readBytes(self, instance, reader):
		pass

	def writeBytes(self, instance, writer):
		writer.putInt16(instance)

class Int32(SerializableIntegralField):
	def readBytes(self, instance, reader):
		pass

	def writeBytes(self, instance, writer):
		writer.putInt32(instance)

# enums

class SerializableEnumField(SerializableIntegralField):
	def __init__(self, cls, *args, **kwargs):
		super().__init__(*args,**kwargs)
		if not issubclass(cls, IntEnum):
			raise ValueError("Uint8Enum needs an IntEnum as class")
		self.cls = cls

	def getInt(self, instance):
		"""
		Checks if the instance represents a valid enumeration value for self.cls
		and returns the int corresponding to this value.
		"""
		if type(instance) is not self.cls:
			# attempt to cast (possibly it was an integer)
			instance = self.cls(instance)
		return int(instance)

class Uint8Enum(SerializableEnumField):
	def readBytes(self, instance, reader):
		pass

	def writeBytes(self, instance, writer):
		# and then cast back to integer and put it into the writer
		writer.putUInt8(self.getInt(instance))



class Uint16Enum(SerializableEnumField):
	def writeBytes(self, instance, writer):
		# and then cast back to integer and put it into the writer
		writer.putUInt16(self.getInt(instance))

# containers

class GenericPacketArray(SerializableField):
	pass

class Variant(SerializableField):
	def __init__(self, typeDict, typeGetter,  *args, **kwargs):
		self.typeDict = typeDict
		self.typeGetter = typeGetter
		self.currentSerializableField = None

	def getCurrentSerializableField(self, parent):
		currentType = self.typeGetter(parent)
		self.currentSerializableField = self.typeDict[currentType]

	def getDefault(self, parent):
		""" obtain current value from the typeGetter and use dict to obtain a default value """
		self.getCurrentSerializableField(parent)
		if self.currentSerializableField is not None:
			return self.currentSerializableField.getDefault(parent)
		else:
			return None

	def writeBytes(self, instance, writer):
		if self.currentSerializableField is not None:
			self.currentSerializableField.writeBytes(instance, writer)
		else:
			print("Warning: Variant cannot writeBytes because c is unknown")



