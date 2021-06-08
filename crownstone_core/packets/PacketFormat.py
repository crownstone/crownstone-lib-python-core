from crownstone_core.util.BufferWriter import BufferWriter

class PacketFormatType:
	"""
	Defines the interface that packets implement.
	"""
	def getPacket(self):
		writer = BufferWriter()
		self.writeBytes(self, writer)
		return writer.getBuffer()

	def loadPacket(self, data):
		pass

	@classmethod
	def getDefault(cls):
		return None

	@classmethod
	def readBytes(cls, instance, reader):
		pass

	def writeBytes(self, instance, writer):
		"""
		Generic implementation: loop over all fields in the instance that are supposed to be serialized
		and call writebytes on the respective type.
		"""
		fields = self.__getattribute__("_serializedFields") or dict()
		for fieldName, fieldType in fields.items():
			fieldType.writeBytes(instance.__dict__[fieldName], writer)


# ----- literal types -------

class Bool(PacketFormatType):
	@classmethod
	def getDefault(cls):
		return False

	@classmethod
	def readBytes(cls, instance, reader):
		pass

	@classmethod
	def writeBytes(cls, instance, writer: BufferWriter):
		writer.putUInt8(instance)

# unsigned ints

class Uint8(PacketFormatType):
	@classmethod
	def getDefault(cls):
		return 8

	@classmethod
	def readBytes(cls, instance, reader):
		pass

	@classmethod
	def writeBytes(cls, instance, writer: BufferWriter):
		writer.putUInt8(instance)

class Uint16(PacketFormatType):
	@classmethod
	def getDefault(cls):
		return 16

	@classmethod
	def readBytes(cls, instance, reader):
		pass

	@classmethod
	def writeBytes(cls, instance, writer: BufferWriter):
		writer.putUInt16(instance)

class Uint32(PacketFormatType):
	@classmethod
	def getDefault(cls):
		return 32

	@classmethod
	def readBytes(cls, instance, reader):
		pass

	@classmethod
	def writeBytes(cls, instance, writer: BufferWriter):
		writer.putUInt32(instance)

# signed ints

class Int8(PacketFormatType):
	@classmethod
	def getDefault(cls):
		return 8

	@classmethod
	def readBytes(cls, instance, reader):
		pass

	@classmethod
	def writeBytes(cls, instance, writer):
		pass

class Int16(PacketFormatType):
	@classmethod
	def getDefault(cls):
		return 16

	@classmethod
	def readBytes(cls, instance, reader):
		pass

	@classmethod
	def writeBytes(cls, instance, writer):
		pass

class Int32(PacketFormatType):
	@classmethod
	def getDefault(cls):
		return 32

	@classmethod
	def readBytes(cls, instance, reader):
		pass

	@classmethod
	def writeBytes(cls, instance, writer):
		pass

# enums

class Uint8Enum(PacketFormatType):
	pass

class Uint16Enum(PacketFormatType):
    pass

# containers

class GenericPacketArray(PacketFormatType):
	pass

class Variant(PacketFormatType):
	def __init__(self, **kwargs):
		pass

