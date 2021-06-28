from crownstone_core.packets.util.GeneratePacketDefinition import CrownstonePacket
from crownstone_core.packets.util.SerializableObject import Uint8
from examples.CrownstonePacketExample import ControlPacket


class MeshCommandPacket(metaclass=CrownstonePacket):
	type = Uint8(0) # Only option for now
	flags = Uint8() # TODO: need a bitmask here
	timeout_or_transmissions = Uint8(0)
	id_count = Uint8(0) # TODO: should be set to len(crownstone_ids)
	crownstone_ids = [] # TODO: need an uint8 array here
	payload = ControlPacket()
