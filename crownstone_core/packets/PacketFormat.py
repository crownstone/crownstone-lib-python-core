from enum import IntEnum

from crownstone_core.util.BufferWriter import BufferWriter
from crownstone_core.util.BufferReader import BufferReader

class SerializableField:
	"""
	Defines the interface that packets implement.
	"""
	def __init__(self, *args, **kwargs):
		pass

	def serialize(self):
		writer = BufferWriter()
		self.writeToBuffer(self, writer)
		return writer.getBuffer()

	def deserialize(self, data):
		reader = BufferReader()
		self.readFromBuffer(self, reader)

	def getDefault(self, parent):
		"""
		Return the default value of this SerializableField.

		Default value of a field is allowed to depend on the siblings of the field.
		E.g. in order to automatically get the length of a variable size array.
		These can be obtains through a reference of the parent.
		"""
		return None

	def readFromBuffer(self, instance, reader):
		"""
		Generic implementation: loop over all fields in the instance that are to be deserialized
		and call readFromBuffer on the respective type.

		instance: the object to deserialize the data into
		writer: the writer to extract the data to deserialize out of
		"""
		for fieldName, fieldType in self.getSerializableFieldDict().items():
			fieldType.readFromBuffer(instance.__dict__[fieldName], reader)

	def writeToBuffer(self, instance, writer: BufferWriter):
		"""
		Generic implementation: loop over all fields in the instance that are to be serialized
		and call writeToBuffer on the respective type.

		instance: the object to serialize
		writer: the writer to serialize the object into
		"""
		for fieldName, fieldType in self.getSerializableFieldDict().items():
			fieldType.writeToBuffer(instance.__dict__[fieldName], writer)

	def getSerializableFieldDict(self):
		return self.__getattribute__("_serializedFields") or dict()


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

	def readFromBuffer(self, instance, reader):
		pass

	def writeToBuffer(self, instance, writer: BufferWriter):
		writer.putUInt8(instance)

# unsigned ints

class Uint8(SerializableIntegralField):
	def readFromBuffer(self, instance, reader):
		pass

	def writeToBuffer(self, instance, writer: BufferWriter):
		writer.putUInt8(instance)

class Uint16(SerializableIntegralField):
	def readFromBuffer(self, instance, reader):
		pass

	def writeToBuffer(self, instance, writer: BufferWriter):
		writer.putUInt16(instance)

class Uint32(SerializableIntegralField):
	def readFromBuffer(self, instance, reader):
		pass

	def writeToBuffer(self, instance, writer: BufferWriter):
		writer.putUInt32(instance)

# signed ints

class Int8(SerializableIntegralField):
	def readFromBuffer(self, instance, reader):
		pass

	def writeToBuffer(self, instance, writer):
		writer.putInt8(instance)

class Int16(SerializableIntegralField):
	def readFromBuffer(self, instance, reader):
		pass

	def writeToBuffer(self, instance, writer):
		writer.putInt16(instance)

class Int32(SerializableIntegralField):
	def readFromBuffer(self, instance, reader):
		pass

	def writeToBuffer(self, instance, writer):
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
	def readFromBuffer(self, instance, reader):
		pass

	def writeToBuffer(self, instance, writer):
		# and then cast back to integer and put it into the writer
		writer.putUInt8(self.getInt(instance))


class Uint16Enum(SerializableEnumField):
	def writeToBuffer(self, instance, writer):
		# and then cast back to integer and put it into the writer
		writer.putUInt16(self.getInt(instance))

# containers

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

	def writeToBuffer(self, instance, writer):
		if self.currentSerializableField is not None:
			self.currentSerializableField.writeToBuffer(instance, writer)
		else:
			print("Warning: Variant cannot writeToBuffer because current type of Variant is unknown")




# class GenericPacketArray(SerializableField):
# 	pass

# TODO: class Uint16AutoSize, Uint16AutoEnum