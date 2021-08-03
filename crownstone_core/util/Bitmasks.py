def set_bit(bitmask: int, bit: int, flag: bool = True) -> int:
    """
    Set a bit in a bitmask.
    :param bitmask:     The initial bitmask.
    :param bit:         The bit to be set.
    :param flag:        True to set the bit high, False to set the bit low.
    :returns:           The updated bitmask.
    """
    if flag:
        bitmask |= (1 << bit)
    else:
        bitmask &= ~(1 << bit)
    return bitmask

def get_bitmask(bits: list) -> int:
    """
    Returns a bitmask with given bits set.
    :param bits:        List of bits to be set.
    :returns:           The bitmask.
    """
    bitmask = 0
    for bit in bits:
        bitmask = set_bit(bitmask, bit)
    return bitmask

class Bitmasks:
    ff64 = 0xffffffffffffffff
    ff32 = 0xffffffff
    ff16 = 0xffff
    ff8  = 0xff