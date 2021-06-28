"""
Concrete base types for SerializableFields.
"""
from crownstone_core.packets.util.SerializableObject import *

# ----- generic (abstract) integral type -----

class SerializableInteger(SerializableObject):
	"""
	Common features for all integral fields.
	"""
	def __init__(self, default=None,  *args, **kwargs):
		super().__init__(*args,**kwargs)
		self.default = kwargs.get("default", default)

	def getDefault(self, parent):
		""" if default is set use that value and transform None into 0 """
		return self.default or 0

# ----- literal (explicit) types -------

class Bool(SerializableInteger):
	def getDefault(self, parent):
		""" if default is set use that value and transform None into False """
		return self.default or False

	def _readFieldFromBuffer(self, reader: BufferReader, parent: 'SerializableObject', fieldType: 'SerializableObject'):
		return True if reader.getUInt8() else False

	def _writeFieldsToBuffer(self, instance, writer: BufferWriter):
		writer.putUInt8(instance)

# unsigned ints

class Uint8(SerializableInteger):
	def _readFieldFromBuffer(self, reader: BufferReader, parent: 'SerializableObject', fieldType: 'SerializableObject'):
		return reader.getUInt8()

	def _writeFieldsToBuffer(self, instance, writer: BufferWriter):
		writer.putUInt8(instance)

class Uint16(SerializableInteger):
	def _readFieldFromBuffer(self, reader: BufferReader, parent: 'SerializableObject', fieldType: 'SerializableObject'):
		return reader.getUInt16()

	def _writeFieldsToBuffer(self, instance, writer: BufferWriter):
		writer.putUInt16(instance)

class Uint32(SerializableInteger):
	def _readFieldFromBuffer(self, reader: BufferReader, parent: 'SerializableObject', fieldType: 'SerializableObject'):
		return reader.getUInt32()

	def _writeFieldsToBuffer(self, instance, writer: BufferWriter):
		writer.putUInt32(instance)

# signed ints

class Int8(SerializableInteger):
	def _readFieldFromBuffer(self, reader: BufferReader, parent: 'SerializableObject', fieldType: 'SerializableObject'):
		return reader.getInt8()

	def _writeFieldsToBuffer(self, instance, writer):
		writer.putInt8(instance)

class Int16(SerializableInteger):
	def _readFieldFromBuffer(self, reader: BufferReader, parent: 'SerializableObject', fieldType: 'SerializableObject'):
		return reader.getInt16()

	def _writeFieldsToBuffer(self, instance, writer):
		writer.putInt16(instance)

class Int32(SerializableInteger):
	def _readFieldFromBuffer(self, reader: BufferReader, parent: 'SerializableObject', fieldType: 'SerializableObject'):
		return reader.getInt32()

	def _writeFieldsToBuffer(self, instance, writer):
		writer.putInt32(instance)

# enums

class SerializableEnum(SerializableInteger):
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

class Uint8Enum(SerializableEnum):
	def _readFieldFromBuffer(self, reader: BufferReader, parent: 'SerializableObject', fieldType: 'SerializableObject'):
		"""
		Converts the next uint8 read from buffer into an instance of type self.cls.
		"""
		return self.cls(reader.getUInt8())

	def _writeFieldsToBuffer(self, instance, writer):
		"""
		Casts the instance to an object of type self.cls,
		converts that to integer and puts it into the writer
		"""
		writer.putUInt8(self.getInt(instance))


class Uint16Enum(SerializableEnum):
	def _readFieldFromBuffer(self, reader: BufferReader, parent: 'SerializableObject', fieldType: 'SerializableObject'):
		return self.cls(reader.getUInt16())

	def _writeFieldsToBuffer(self, instance, writer):
		# and then cast back to integer and put it into the writer
		writer.putUInt16(self.getInt(instance))
