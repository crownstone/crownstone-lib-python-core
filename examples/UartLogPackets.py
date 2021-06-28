from crownstone_core.packets.util.GeneratePacketDefinition import CrownstonePacket
from crownstone_core.packets.util.SerializableObject import Uint32, Uint16, Uint8


class UartLogHeaderPacket(metaclass=CrownstonePacket):
	fileNameHash = Uint32()
	lineNr = Uint16()
	logLevel = Uint8()
	flags = Uint8()

class UartLogPacket(metaclass=CrownstonePacket):
	header = UartLogHeaderPacket()
	argCount = Uint8()
	# TODO: need a list of UartLogArgPackets here.

class UartLogArgPacket(metaclass=CrownstonePacket):
	argSize = Uint8()
	argData = list # TODO: need a list of bytes here.
