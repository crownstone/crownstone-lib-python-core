from crownstone_core.util.DataStepper import DataStepper
from crownstone_core.protocol.BluenetTypes import PowerSamplesType
from crownstone_core.Exceptions import CrownstoneError, CrownstoneException

class PowerSamplesPacket:
	def __init__(self, data):
		self.samplesType = PowerSamplesType.UNSPECIFIED
		self.index = 0            # uint8
		self.count = 0            # uint16
		self.timestamp = 0        # uint32
		self.delayUs = 0          # uint16
		self.sampleIntervalUs = 0 # uint16
		self.reserved = 0         # 2 bytes
		self.offset = 0           # int16
		self.multiplier = 0.0     # float

		self.samples = []         # int16 list
		self.load(data)

	def load(self, data):
		headerSize = 1 + 1 + 2 + 4 + 2 + 2 + 2 + 2 + 4
		if (len(data) < headerSize):
			raise CrownstoneException(CrownstoneError.INCORRECT_RESPONSE_LENGTH, "Data size too small for header")
		streamBuf = DataStepper(data)
		self.samplesType = PowerSamplesType(streamBuf.getUInt8())
		self.index = streamBuf.getUInt8()
		self.count = streamBuf.getUInt16()
		self.timestamp = streamBuf.getUInt32()
		self.delayUs = streamBuf.getUInt16()
		self.sampleIntervalUs = streamBuf.getUInt16()
		streamBuf.skip(2)
		self.offset = streamBuf.getInt16()
		self.multiplier = streamBuf.getFloat()
		if (streamBuf.remaining() < self.count * 2):
			raise CrownstoneException(CrownstoneError.INCORRECT_RESPONSE_LENGTH, "Data size too small for samples")
		self.samples = []
		for i in range(0, self.count):
			self.samples.append(streamBuf.getInt16())

	def toString(self):
		msg = "PowerSamplesPacket("
		msg += "type=" + str(self.samplesType)
		msg += " count=" + str(self.count)
		msg += " timestamp=" + str(self.timestamp)
		msg += " delayUs=" + str(self.delayUs)
		msg += " sampleIntervalUs=" + str(self.sampleIntervalUs)
		msg += " offset=" + str(self.offset)
		msg += " multiplier=" + str(self.multiplier)
		msg += " samples=" + str(self.samples)
		msg += ")"
		return msg

	def __str__(self):
		return self.toString()