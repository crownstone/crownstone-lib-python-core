from crownstone_core.util.DataStepper import DataStepper

class BasePacket:
	def _parse(self, dataStepper: DataStepper):
		"""
		The function to be implemented by derived classes.
		:param dataStepper: The data to be parsed.
		"""
		raise NotImplementedError

	def parse(self, data):
		if isinstance(data, DataStepper):
			self._parse(data)
		elif isinstance(data, list):
			dataStepper = DataStepper(data)
			self._parse(dataStepper)
		else:
			raise TypeError
