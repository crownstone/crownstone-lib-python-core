"""
An class decorator that helps to define packet formats in short and concise fashion.

Example usage can (for now) be found in CrownstonePacketExample.py
"""
from crownstone_core.packets.util.SerializableObject import *

def GenerateSerializableObject(cls):
    """
    This class decorator creates or adjusts a class's __init__ method so that when initializing:
     - if a custom __init__ is defined, first call this
     - for any class field of type SerializableObject
        - if the instance field is constructed by the custom init, don't touch it.
        - elif there is a keyword argument for this field, set the instance field accordingly.
        - elif there is a positional argument, pop that and use that to set the instance field.
        - else use the SerializableObject to construct a default value.
    """
    if not issubclass(cls, SerializableObject):
        raise AttributeError("Packet definitions can only be generated for SerializableObjects")
    # add a wrapper to __init__ that initializes the objects serializable fields and
    # add the dict defining which fields are to be serialized to the class variables.
    originalInit = getattr(cls, "__init__", None)
    cls.__init__ = _makeInitMethod(originalInit)

    return cls


def _makeInitMethod(customInit = None):
    def initmethod(self, *args, **kwargs):
        if customInit:
            customInit(self, *args, **kwargs)

        # For fields that haven't been constructed by customInit:
        # - check if there's a keyword argument to assign
        # - check if there is a positiional argument to assign
        # - construct a new object from fieldType.getDefault

        args_generator = (x for x in args)
        for fieldName, fieldType in self.getSerializableFields():
            print("serializable field:", fieldName)
            # if getattr(self, fieldName, None) is None:
            if fieldName not in self.__dict__:
                field = None
                if field is None and kwargs:
                    field = kwargs.pop(fieldName, None)
                if field is None and args:
                    field = next(args_generator, None)
                if field is None:
                    field = fieldType.getDefault(parent=self)
                print("boo")
                setattr(self, fieldName, field)

        # anything unused keyword arguments indicates wrongly constructed object.
        if kwargs:
            raise AttributeError(F"{self.__class__} does not contain an attributes for {kwargs}")

        # same for positional arguments.
        if next(args_generator, None) is not None:
            raise AttributeError(F"{self.__class__} too many positional arguments provided")

    return initmethod
