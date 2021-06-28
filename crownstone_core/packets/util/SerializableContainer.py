from crownstone_core.packets.util.SerializableObject import *

# containers

class SerializableUnion(SerializableObject):
	def __init__(self, typeDict, typeGetter,  *args, **kwargs):
		"""
		typeDict: a dict mapping values to SerializableObject instances.
		typeGetter: a delegate that receives the parent of this object and should return
			a key in the typeDict or None.
		"""
		self.typeDict = typeDict
		self.typeGetter = typeGetter
		self.currentSerializableField = None

	def getCurrentSerializableField(self, parent):
		currentType = self.typeGetter(parent)
		self.currentSerializableField = self.typeDict[currentType]

	def getDefault(self, parent):
		""" obtain current value from the typeGetter and use typeDict to obtain a default value """
		if parent is None:
			raise ValueError("SerializableUnion needs a parent to construct a default object")

		self.getCurrentSerializableField(parent)
		if self.currentSerializableField is not None:
			return self.currentSerializableField.getDefault(parent)
		else:
			return None

	def _writeFieldsToBuffer(self, instance, writer):
		if self.currentSerializableField is not None:
			self.currentSerializableField._writeFieldsToBuffer(instance, writer)
		else:
			print("Warning: Variant cannot writeFieldsToBuffer because current type of Variant is unknown")

	def _readFieldFromBuffer(self, reader: BufferReader, parent: 'SerializableObject', fieldType: 'SerializableObject'):
		""" forwards reading the field to the currentSerializableField """
		self.getCurrentSerializableField(parent)
		return self.currentSerializableField._readFieldFromBuffer(reader, parent=parent, fieldType=fieldType)

# class GenericPacketArray(SerializableObject):
# 	pass

# TODO: class Uint16AutoSize, Uint16AutoEnum, Variant with some fieldType=None enum values.