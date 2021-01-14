from crownstone_core.util.DataStepper import DataStepper
from crownstone_core.protocol.BluenetTypes import PowerSamplesType
from crownstone_core.Exceptions import CrownstoneError, CrownstoneException

class AdcRestartsPacket:
	def __init__(self, data):
		self.count = 0            # uint32
		self.timestamp = 0        # uint32
		self.load(data)

	def load(self, data):
		"""
		Parses data buffer to set member variables.

		data : list of bytes

		Raises exception when parsing fails.
		"""
		streamBuf = DataStepper(data)
		self.count = streamBuf.getUInt32()
		self.timestamp = streamBuf.getUInt32()

	def toString(self):
		msg = "AdcRestartsPacket("
		msg += "count=" + str(self.count)
		msg += " timestamp=" + str(self.timestamp)
		msg += ")"
		return msg

	def __str__(self):
		return self.toString()