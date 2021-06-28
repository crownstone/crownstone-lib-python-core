from enum import IntEnum
import inspect

from crownstone_core.util.BufferWriter import BufferWriter
from crownstone_core.util.BufferReader import BufferReader


class SerializableObject:
    def getSerializableFields(self):
        return inspect.getmembers(type(self),
				  predicate=lambda member: issubclass(type(member), SerializableObject))

# TODO: change implementation to work with GeneratePacketDefinition decorator.
class SerializableField:
    """
    Defines the interface that packets implement.
    """
    def __init__(self, *args, **kwargs):
        pass

    def serialize(self):
        writer = BufferWriter()
        self.writeFieldsToBuffer(self, writer)
        return writer.getBuffer()

    def deserialize(self, data):
        reader = BufferReader(data)
        self.readFieldsFromBuffer(reader, parent=None)

    def getDefault(self, parent):
        """
        Return the default value of this SerializableField.

        Default value of a field is allowed to depend on the siblings of the field.
        E.g. in order to automatically get the length of a variable size array.
        These can be obtains through a reference of the parent.
        """
        return self

    def readFieldsFromBuffer(self, reader: BufferReader, parent: 'SerializableField'):
        """
        Generic implementation:
        for each field of `self` that is to be deserialized:
         - construct a the default object of that type and
         - call readFieldsFromBuffer on the newly constructed object.

        reader: the reader to extract the data to deserialize out of
        """
        # load all serializable fields from the reader
        for fieldName, fieldType in self.getSerializableFieldDict().items():
            field = self.readFieldFromBuffer(reader, parent, fieldType)
            setattr(self, fieldName, field)
        return self

    def readFieldFromBuffer(self, reader: BufferReader, parent: 'SerializableField', fieldType: 'SerializableField'):
        """
        Return an object constructed from the information in the buffer

        fieldType is None for 'leaf fieldTypes'
        """
        field = fieldType.getDefault(parent=self)
        if issubclass(type(field), SerializableField):
            # E.g.: type(fieldType) == SunTimes and type(field) == Sun
            # the field can handle the deserialization itself.
            # the ancestor hierarchy is: parent > self > field
            field.readFieldsFromBuffer(reader, parent=self)
        else:
            # E.g.: type(fieldType) == Uint8 and type(field) == int
            # the fieldType needs to assign the field in this scope.
            # as `field` can't be passed by reference.
            field = fieldType.readFieldFromBuffer(reader, parent=self, fieldType=None)
        return field

    def writeFieldsToBuffer(self, instance, writer: BufferWriter):
        """
        Generic implementation: loop over all fields in the instance that are to be serialized
        and call writeFieldsToBuffer on the respective type.

        instance: the object to serialize
        writer: the writer to serialize the object into
        """
        for fieldName, fieldType in self.getSerializableFieldDict().items():
            fieldType.writeFieldsToBuffer(instance.__dict__[fieldName], writer)

    def getSerializableFieldDict(self):
        return getattr(self,"_serializedFields", dict())

