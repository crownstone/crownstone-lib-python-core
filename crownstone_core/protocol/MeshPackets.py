

from enum import IntEnum
from typing import List

from crownstone_core.Exceptions import CrownstoneException, CrownstoneError

from crownstone_core.protocol.BluenetTypes import ControlType

# broadcast to all:
# value: 1
#
# broadcast to all, but retry until ID's in list have acked or timeout
# value: 3
#
# 1:1 message to N crownstones with acks (only N = 1 supported for now)
# value: 2

class MeshModes(IntEnum):
    BROADCAST           = 1
    SINGLE_TARGET_ACKED = 2
    BROADCAST_ACKED_IDS = 3


class _MeshCommandPacket:

    def __init__(self, packetType, crownstoneIds : List[int], payload, mesh_command_mode, timeout_or_transmissions):
        self.type = packetType
        self.crownstoneIds = crownstoneIds
        self.payload = payload
        self.flags = mesh_command_mode.value
        self.timeout_or_transmissions = timeout_or_transmissions

    def getPacket(self):
        packet = []
        packet.append(self.type)
        packet.append(self.flags)
        packet.append(self.timeout_or_transmissions)
        packet.append(len(self.crownstoneIds))
        packet += self.crownstoneIds
        packet += self.payload

        return packet

class MeshBroadcast(_MeshCommandPacket):

    def __init__(self, packetType, payload, timeout ):
        if packetType != ControlType.SET_TIME and packetType != ControlType.NO_OPERATION:
            raise CrownstoneException(CrownstoneError.NOT_IMPLEMENTED_YET, "Currently only the SET_TIME and NO_OPERATION is supported by MeshBroadcast.")
        super().__init__(packetType, [], payload, MeshModes.BROADCAST, timeout)

class MeshSetState(_MeshCommandPacket):

    def __init__(self, crownstoneId : int, setStatePacket, numberOfAttempts = 0 ):
        """
        Attempts 0 uses the default amount of attempts
        """
        super().__init__(ControlType.SET_STATE, [crownstoneId], setStatePacket, MeshModes.SINGLE_TARGET_ACKED, numberOfAttempts)

class MeshBroadcastAcked(_MeshCommandPacket):
    """
    This is currently only supported for type setIBeaconConfig
    """
    def __init__(self, packetType, crownstoneIds: List[int], payload, numberOfAttempts):
        if packetType != ControlType.SET_IBEACON_CONFIG_ID:
            raise CrownstoneException(CrownstoneError.NOT_IMPLEMENTED_YET, "Currently only the SET_IBEACON_CONFIG_ID is supported by Mesh Broadcast Acked.")
        super().__init__(packetType, crownstoneIds, payload, MeshModes.BROADCAST_ACKED_IDS, numberOfAttempts)


class StoneMultiSwitchPacket:

    def __init__(self, crownstoneId, state):
        """
        :param crownstoneId:
        :param state:  number [0..1]

        """
        self.crownstoneId = crownstoneId
        self.state = int(min(1, max(0, state)) * 100) # map to [0 .. 100]


    def getPacket(self):
        packet = []
        packet.append(self.crownstoneId)
        packet.append(self.state)

        return packet


class MeshMultiSwitchPacket:

    def __init__(self, packets = []):
        self.packets = packets

    def getPacket(self):
        packet = []
        packet.append(len(self.packets))
        for stonePacket in self.packets:
            packet += stonePacket.getPacket()

        return packet