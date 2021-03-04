
from crownstone_core.packets.Advertisement import Advertisement

from crownstone_core.packets.serviceDataParsers.parsers import parseOpcode7
from crownstone_core.packets.ServiceData import ServiceData

def test_serviceData():
    payload = [7,4,2,70,0,179,39,127,231,255,6,153,1,0,217,153,0,250]
    assert(len(payload) == 18)
    serviceData = ServiceData(payload)
    serviceData.parse()
    assert(serviceData.payload.crownstoneId == 70)

    assert(hasattr(serviceData.payload,"crownstoneId"))
    assert(hasattr(serviceData.payload,"blub") == False)

def test_AdvClasses():
    payload = [2,70,0,179,39,127,231,255,6,153,1,0,217,153,0,250]
    assert(len(payload) == 16)
    result = parseOpcode7(payload)
    assert(result.timestamp == 1614846425)

def test_advertisement():
    address = "65D492A1-E3ED-418D-BF98-07EFBEC8D9A7"
    rssi = "-79"
    nameText = "CRWN"
    serviceDataArray = [7, 5, 149, 136, 10, 129, 31, 42, 16, 242, 107, 133, 131, 103, 174, 129, 126, 184]
    serviceUUID = 49153
    advertisement = Advertisement(address, rssi, nameText, serviceDataArray, serviceUUID)

def test_decryptingServiceData():
    key = bytearray(b'\xea K\x7fE\xf4`E\xfe\x95\xbc\xbcG)\x95\x80')
    data = [7, 5, 56, 17, 1, 68, 239, 118, 130, 213, 132, 22, 52, 247, 165, 153, 166, 56]
    serviceData = ServiceData(data)
    serviceData.parse(key)
    assert serviceData.decrypted

