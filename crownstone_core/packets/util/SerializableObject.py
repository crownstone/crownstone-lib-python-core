from enum import IntEnum
import inspect

from crownstone_core.util.BufferWriter import BufferWriter
from crownstone_core.util.BufferReader import BufferReader

class SerializableObject:
    """
    Defines the interface that packets implement.

    descriptor: an optional argument that can be used to differentiate/identify fields.
    """
    def __init__(self, descriptor=None, *args, **kwargs):
        self.descriptor = descriptor

    def serialize(self):
        """
        Constructs a bufferwriter and then loops through all the serialisable fields of this object.
        """
        writer = BufferWriter()
        self._writeFieldsToBuffer(self, writer, None)
        return writer.getBuffer()

    def deserialize(self, data):
        reader = BufferReader(data)
        self._deserializeFromBuffer(reader, parent=self)

    def getDefault(self, parent=None):
        """
        Return the default value of this SerializableField.

        Default value of a field is allowed to depend on the siblings of the field.
        E.g. in order to automatically get the length of a variable size array.
        These can be obtains through a reference of the parent.
        """
        return self

    def getSerializableFields(self):
        return [(n, v) for n,v in type(self).__dict__.items() if isSerializable(v)]

    def _writeFieldsToBuffer(self, instance, writer: BufferWriter, parent: 'SerializableObject'):
        """
        Generic implementation: loop over all fields in the instance that are to be serialized
        and call writeFieldsToBuffer on the respective type.

        Subclasses of SerializableObject may overwrite this method to serialize non-serializable objects.
        E.g.: see SerializableInteger.Uint8.

        instance: the object to serialize
        writer: the writer to serialize the object into
        """
        for fieldName, serializer in self.getSerializableFields():
            print("serializing: ", fieldName)
            serializer._writeFieldsToBuffer(
                getattr(instance, fieldName),
                writer,
                self)

    def _deserializeFromBuffer(self, reader: BufferReader, parent: 'SerializableObject'=None):
        """ deserializeFromReader """
        for name, serializer in self.getSerializableFields():
            field = serializer._deserializeFromBuffer(reader, parent=self)
            setattr(self, name, field)
        return self

def isSerializable(obj):
    return issubclass(type(obj), SerializableObject)
