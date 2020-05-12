
class MeshCommandPacket:
    type = 0
    bitmask = 0
    crownstoneIds = []
    payload = []

    def __init__(self, packetType, crownstoneIds, payload):
        self.type = packetType
        self.crownstoneIds = crownstoneIds
        self.payload = payload

    def getPacket(self):
        packet = []
        packet.append(self.type)
        packet.append(self.bitmask)
        packet.append(len(self.crownstoneIds))
        packet += self.crownstoneIds
        packet += self.payload

        return packet


class StoneMultiSwitchPacket:
    crownstoneId = 0
    state = 0

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
    packets = []

    def __init__(self, packets):
        self.packets = packets

    def getPacket(self):
        packet = []
        packet.append(len(self.packets))
        for stonePacket in self.packets:
            packet += stonePacket.getPacket()

        return packet