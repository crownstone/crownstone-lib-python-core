from crownstone_core.packets.serviceDataParsers.parsers import parseOpcode7
from crownstone_core.packets.ServiceData import ServiceData

def test_serviceData():
    payload = [7,4,2,70,0,179,39,127,231,255,6,153,1,0,217,153,0,250]
    assert(len(payload) == 18)
    serviceData = ServiceData(payload)
    assert(serviceData.payload.crownstoneId == 70)

    assert(hasattr(serviceData.payload,"crownstoneId"))
    assert(hasattr(serviceData.payload,"blub") == False)

def test_AdvClasses():
    payload = [2,70,0,179,39,127,231,255,6,153,1,0,217,153,0,250]
    assert(len(payload) == 16)
    result = parseOpcode7(payload)
    assert(result.timestamp == 1614780889)

