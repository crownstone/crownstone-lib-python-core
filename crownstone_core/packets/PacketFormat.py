from enum import IntEnum

from crownstone_core.util.BufferWriter import BufferWriter

class PacketFormatType:
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

	def getDefault(self):
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

class IntegralPacketFormatType(PacketFormatType):
	def __init__(self, default=None,  *args, **kwargs):
		super().__init__(*args,**kwargs)
		self.default = kwargs.get("default", default)

	def getDefault(self):
		return self.default or 0

# ----- literal types -------

class Bool(IntegralPacketFormatType):
	def getDefault(self):
		return self.default or False

	def readBytes(self, instance, reader):
		pass

	def writeBytes(self, instance, writer: BufferWriter):
		writer.putUInt8(instance)

# unsigned ints

class Uint8(IntegralPacketFormatType):
	def getDefault(self):
		return 8

	def readBytes(self, instance, reader):
		pass

	def writeBytes(self, instance, writer: BufferWriter):
		writer.putUInt8(instance)

class Uint16(IntegralPacketFormatType):
	def getDefault(self):
		return 16

	def readBytes(self, instance, reader):
		pass

	def writeBytes(self, instance, writer: BufferWriter):
		writer.putUInt16(instance)

class Uint32(IntegralPacketFormatType):
	def getDefault(self):
		return 32

	def readBytes(self, instance, reader):
		pass

	def writeBytes(self, instance, writer: BufferWriter):
		writer.putUInt32(instance)

# signed ints

class Int8(IntegralPacketFormatType):
	def getDefault(self):
		return 8

	def readBytes(self, instance, reader):
		pass

	def writeBytes(self, instance, writer):
		writer.putInt8(instance)

class Int16(IntegralPacketFormatType):
	def getDefault(self):
		return 16

	def readBytes(self, instance, reader):
		pass

	def writeBytes(self, instance, writer):
		writer.putInt16(instance)

class Int32(IntegralPacketFormatType):
	def getDefault(self):
		return 32

	def readBytes(self, instance, reader):
		pass

	def writeBytes(self, instance, writer):
		writer.putInt32(instance)

# enums

class EnumPacketFormatType(IntegralPacketFormatType):
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

class Uint8Enum(EnumPacketFormatType):
	def readBytes(self, instance, reader):
		pass

	def writeBytes(self, instance, writer):
		# and then cast back to integer and put it into the writer
		writer.putUInt8(self.getInt(instance))



class Uint16Enum(PacketFormatType):
    pass

# containers

class GenericPacketArray(PacketFormatType):
	pass

class Variant(PacketFormatType):
	def __init__(self, **kwargs):
		pass

