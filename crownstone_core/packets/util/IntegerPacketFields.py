from crownstone_core.packets.util.PacketField import *



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
