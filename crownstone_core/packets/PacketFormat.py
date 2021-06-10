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
		self.writeFieldsToBuffer(self, writer)
		return writer.getBuffer()

	def deserialize(self, data):
		reader = BufferReader(data)
		self.readFieldsFromBuffer(reader, parent=None)

	def getDefault(self, parent):
		"""
		Return the default value of this SerializableField.

		Default value of a field is allowed to depend on the siblings of the field.
		E.g. in order to automatically get the length of a variable size array.
		These can be obtains through a reference of the parent.
		"""
		return self

	def readFieldsFromBuffer(self, reader: BufferReader, parent: 'SerializableField'):
		"""
		Generic implementation:
		for each field of `self` that is to be deserialized:
		 - construct a the default object of that type and
		 - call readFieldsFromBuffer on the newly constructed object.

		reader: the reader to extract the data to deserialize out of
		"""
		# load all serializable fields from the reader
		for fieldName, fieldType in self.getSerializableFieldDict().items():
			field = self.readFieldFromBuffer(reader, parent, fieldType)
			setattr(self, fieldName, field)
		return self

	def readFieldFromBuffer(self, reader: BufferReader, parent: 'SerializableField', fieldType: 'SerializableField'):
		"""
		Return an object constructed from the information in the buffer

		fieldType is None for 'leaf fieldTypes'
		"""
		field = fieldType.getDefault(parent=self)
		if issubclass(type(field), SerializableField):
			# E.g.: type(fieldType) == SunTimes and type(field) == Sun
			# the field can handle the deserialization itself.
			# the ancestor hierarchy is: parent > self > field
			field.readFieldsFromBuffer(reader, parent=self)
		else:
			# E.g.: type(fieldType) == Uint8 and type(field) == int
			# the fieldType needs to assign the field in this scope.
			# as `field` can't be passed by reference.
			field = fieldType.readFieldFromBuffer(reader, parent=self, fieldType=None)
		return field

	def writeFieldsToBuffer(self, instance, writer: BufferWriter):
		"""
		Generic implementation: loop over all fields in the instance that are to be serialized
		and call writeFieldsToBuffer on the respective type.

		instance: the object to serialize
		writer: the writer to serialize the object into
		"""
		for fieldName, fieldType in self.getSerializableFieldDict().items():
			fieldType.writeFieldsToBuffer(instance.__dict__[fieldName], writer)

	def getSerializableFieldDict(self):
		return getattr(self,"_serializedFields", dict())


# ----- generic (abstract) integral type -----

class SerializableIntegralField(SerializableField):
	def __init__(self, default=None,  *args, **kwargs):
		super().__init__(*args,**kwargs)
		self.default = kwargs.get("default", default)

	def getDefault(self, parent):
		""" if default is set use that value and transform None into 0 """
		return self.default or 0

# ----- literal (explicit) types -------

class Bool(SerializableIntegralField):
	def getDefault(self, parent):
		""" if default is set use that value and transform None into False """
		return self.default or False

	def readFieldFromBuffer(self, reader: BufferReader, parent: 'SerializableField', fieldType: 'SerializableField'):
		return True if reader.getUInt8() else False

	def writeFieldsToBuffer(self, instance, writer: BufferWriter):
		writer.putUInt8(instance)

# unsigned ints

class Uint8(SerializableIntegralField):
	def readFieldFromBuffer(self, reader: BufferReader, parent: 'SerializableField', fieldType: 'SerializableField'):
		return reader.getUInt8()

	def writeFieldsToBuffer(self, instance, writer: BufferWriter):
		writer.putUInt8(instance)

class Uint16(SerializableIntegralField):
	def readFieldFromBuffer(self, reader: BufferReader, parent: 'SerializableField', fieldType: 'SerializableField'):
		return reader.getUInt16()

	def writeFieldsToBuffer(self, instance, writer: BufferWriter):
		writer.putUInt16(instance)

class Uint32(SerializableIntegralField):
	def readFieldFromBuffer(self, reader: BufferReader, parent: 'SerializableField', fieldType: 'SerializableField'):
		return reader.getUInt32()

	def writeFieldsToBuffer(self, instance, writer: BufferWriter):
		writer.putUInt32(instance)

# signed ints

class Int8(SerializableIntegralField):
	def readFieldFromBuffer(self, reader: BufferReader, parent: 'SerializableField', fieldType: 'SerializableField'):
		return reader.getInt8()

	def writeFieldsToBuffer(self, instance, writer):
		writer.putInt8(instance)

class Int16(SerializableIntegralField):
	def readFieldFromBuffer(self, reader: BufferReader, parent: 'SerializableField', fieldType: 'SerializableField'):
		return reader.getInt16()

	def writeFieldsToBuffer(self, instance, writer):
		writer.putInt16(instance)

class Int32(SerializableIntegralField):
	def readFieldFromBuffer(self, reader: BufferReader, parent: 'SerializableField', fieldType: 'SerializableField'):
		return reader.getInt32()

	def writeFieldsToBuffer(self, instance, writer):
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
	def readFieldFromBuffer(self, reader: BufferReader, parent: 'SerializableField', fieldType: 'SerializableField'):
		return self.cls(reader.getUInt8())

	def writeFieldsToBuffer(self, instance, writer):
		# and then cast back to integer and put it into the writer
		writer.putUInt8(self.getInt(instance))


class Uint16Enum(SerializableEnumField):
	def readFieldFromBuffer(self, reader: BufferReader, parent: 'SerializableField', fieldType: 'SerializableField'):
		return self.cls(reader.getUInt16())

	def writeFieldsToBuffer(self, instance, writer):
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

	def writeFieldsToBuffer(self, instance, writer):
		if self.currentSerializableField is not None:
			self.currentSerializableField.writeFieldsToBuffer(instance, writer)
		else:
			print("Warning: Variant cannot writeFieldsToBuffer because current type of Variant is unknown")

	def readFieldFromBuffer(self, reader: BufferReader, parent: 'SerializableField', fieldType: 'SerializableField'):
		""" forwards reading the field to the currentSerializableField """
		self.getCurrentSerializableField(parent)
		return self.currentSerializableField.readFieldFromBuffer(reader,parent=parent, fieldType=fieldType)


# class GenericPacketArray(SerializableField):
# 	pass

# TODO: class Uint16AutoSize, Uint16AutoEnum