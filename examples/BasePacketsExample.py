from crownstone_core.packets.cuckoofilter.BasePackets import *

# ------------------------------------------
# --- custom example packet definitions ----
# ------------------------------------------

class SomePacket(PacketBase):               # basic example packet
    def __init__(self, x=0, y=0):
        self.x = Uint8(x)
        self.y = Uint16(y)

class Fruit(CsUint8Enum):                   # PacketBase is enum friendly
    APPLE = 0
    BANANA = 1
    CANTALOUPE = 2

class DerrivedPacket(SomePacket):           # PacketBase is inheritance friendly
    def __init__(self, z=0):
        super().__init__(0xab, 0xcdef)      # non default values if you want them. (can be left out)
        self.z = Uint16(z)

class CompositePacket(PacketBase):          # PacketBase is composition friendly
    def __init__(self):
        self.t = Fruit.BANANA
        self.b = SomePacket()
        self.a = DerrivedPacket()
        self.l = Uint8Array()

class AliasPacket(Uint8Array):              # PacketBase is alias friendly
    pass

class EmptyPacket(PacketBase):              # PacketBase is empty packet friendly
    def doSometing(self):                   # even if you add methods
        print("empty packet says: hi!")

# ---------------------------------------
# ------------ example usage ------------
# ---------------------------------------

if __name__ == "__main__":
    s = SomePacket(0xab, 0xabcd)
    s.x = 3  # overwrite .x, leave y as constructed.

    print("some packet: " , s)
    print("some packet:      ", [hex(x) for x in s.getPacket()])

    a = AliasPacket([8, 7, 6, 5, 4, 3, 23, 2])

    print()
    print("alias packet", a)
    print("alias packet:     ", [hex(x) for x in a.getPacket()])

    empty = EmptyPacket()
    print()
    empty.doSometing()
    print("empty packet:", empty)
    print("empty packet: ", empty.getPacket())

    d = DerrivedPacket()
    d.x = 1
    d.y = 0x4567
    d.z = d.y

    print()
    print("derrived packet: ", d)
    print("derrived packet:            ", [hex(x) for x in d.getPacket()])
    print("expanded derrivedpacket:  ",
          [hex(x) for x in d.x.getPacket()],
          [hex(x) for x in d.y.getPacket()],
          [hex(x) for x in d.z.getPacket()])

    c = CompositePacket()
    c.a = d
    c.b = s
    c.l = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]

    print()
    print("composite packet:", c)
    print("composite packet:             ", [hex(x) for x in c.getPacket()])
    print("expanded composite packet: ",
          [hex(x) for x in c.t.getPacket()],
          [hex(x) for x in c.b.getPacket()],
          [hex(x) for x in c.a.getPacket()],
          [hex(x) for x in c.l.getPacket()])