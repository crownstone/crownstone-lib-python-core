from crownstone_core.util.BasePackets import *

def test_PacketBase():

    class TestPacket(PacketBase):

        def __init__(self, a = None, b = None, c = None):
            self.a = Uint8(a)
            self.b = Uint16(b)
            self.c = Uint32(c)

    test = TestPacket(1,2,3)
    packet = test.getPacket()

    empty = TestPacket()

    empty.fromData(packet)
    assert empty.a.val == 1
    assert empty.b.val == 2
    assert empty.c.val == 3
