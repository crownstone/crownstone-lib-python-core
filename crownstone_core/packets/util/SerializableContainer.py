from crownstone_core.packets.util.SerializableObject import *

# containers

# TODO: rename
class SerializableUnion(SerializableField):
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

# TODO: class Uint16AutoSize, Uint16AutoEnum, Variant with some fieldType=None enum values.