class Bitmasks:
    ff64 = 0xffffffffffffffff
    ff32 = 0xffffffff
    ff16 = 0xffff
    ff8  = 0xff


def set_bit(bitmask: int, bit: int, flag: bool = True) -> int:
    if flag:
        bitmask |= (1 << bit)
    return bitmask
