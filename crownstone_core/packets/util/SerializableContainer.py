from crownstone_core.packets.util.SerializableObject import *
from typing import Tuple

class SerializableUnion(SerializableObject):
	def __init__(self, typeGetter, *args, **kwargs):
		"""
		typeDict: a dict mapping values to SerializableObject instances.
		typeGetter: a delegate that receives the parent of this object and should return
			a key in the typeDict or None.
		"""
		typeGetter = typeGetter or kwargs.get("typeGetter", None)
		if typeGetter is None:
			raise ValueError("SerializableUnion.typeGetter must be a callable object")

		self.typeGetter = typeGetter
		self._currentType = None

	def loadCurrentType(self, parent):
		if parent is None:
			raise ValueError("SerializableUnion cannot identify current type without parent")
		# pass the class of the parent to the type getter to obtain
		# the serializable field instance that describes how to handle serialization.
		self._currentType = self.typeGetter(parent)

	def getCurrentFieldNameAndSerializer(self) -> Tuple[str, SerializableObject]:
		"""
		Uses _currentType to obtains the actual value of this Union by looping over
		the SerializableFields contained in this object and checking for a descriptor match.

		Does not call loadCurrentType as it isn't given a parent parameter.
		If no match is found, None is returned.
		"""
		for name,serializer in self.getSerializableFields():
			if serializer.descriptor == self._currentType:
				return name, serializer
		return None, None

	def getDefault(self, parent):
		"""
		An instance of SerializableUnion contains defaults for all the subfields.
		"""
		return self

	def _writeFieldsToBuffer(self, instance, writer: BufferWriter, parent: 'SerializableObject'):
		"""
		Check which union member needs to be serialized and then forward the _write call
		to that serializer and instance.
		"""
		self.loadCurrentType(parent)
		name, serializer = self.getCurrentFieldNameAndSerializer()
		# print("Union writeFields",self._currentType, serializer)
		# print(instance,".",name)
		# print(getattr(instance, name, "can't find it"))
		if serializer is not None:
			serializer._writeFieldsToBuffer(getattr(instance, name, None), writer, self) # TODO: check parent
		else:
			print("SerializableUnion cannot writeFieldsToBuffer, _currentObjectSerializer is None.")

	def _deserializeFromBuffer(self, reader: BufferReader, parent: 'SerializableObject'):
		"""
		forwards reading the field to the currentSerializableField
		"""
		self.loadCurrentType(parent)
		name, serializer = self.getCurrentFieldNameAndSerializer()
		val = serializer._deserializeFromBuffer(reader, parent)
		setattr(self,name,val)
		return self


# class GenericPacketArray(SerializableObject):
# 	pass

# TODO: class Uint16AutoSize, Uint16AutoEnum, Variant with some fieldType=None enum values.