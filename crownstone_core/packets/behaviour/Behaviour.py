#
#  Behaviour.swift
#  CrownstoneCore
#
#  Created by Alex de Mulder on 22/10/2019.
#  Copyright © 2019 Alex de Mulder. All rights reserved.
#
from crownstone_core.packets.behaviour.BehaviourBase import BehaviourBase, DEFAULT_ACTIVE_DAYS, DEFAULT_TIME
from crownstone_core.packets.behaviour.BehaviourTypes import BehaviourType
from crownstone_core.packets.behaviour.PresenceDescription import BehaviourPresence, BehaviourPresenceType, \
    DEFAULT_PRESENCE_DELAY

DEFAULT_PRESENCE = BehaviourPresence().setSpherePresence(BehaviourPresenceType.someoneInSphere)


class Behaviour(BehaviourBase):

    def __init__(self, profileIndex=0, behaviourType=BehaviourType.behaviour, intensity=100,
                 activeDays=DEFAULT_ACTIVE_DAYS, time=DEFAULT_TIME, presence=DEFAULT_PRESENCE, endCondition=None,
                 idOnCrownstone=None):
        super().__init__(profileIndex, behaviourType, intensity, activeDays, time, presence, endCondition,
                         idOnCrownstone)

    def ignorePresence(self):
        self.presence = None
        return self

    def setPresenceIgnore(self):
        return self.ignorePresence()

    def setPresenceSomebody(self):
        self.setPresenceSomebodyInSphere()
        return self

    def setPresenceNobody(self):
        self.setPresenceNobodyInSphere()
        return self

    def setPresenceSomebodyInSphere(self):
        self.presence = BehaviourPresence().setSpherePresence(BehaviourPresenceType.someoneInSphere)
        return self

    def setPresenceNobodyInSphere(self):
        self.presence = BehaviourPresence().setSpherePresence(BehaviourPresenceType.nobodyInSphere)
        return self

    def setPresenceInSphere(self):
        self.setPresenceSomebodyInSphere()
        return self

    def setPresenceInLocations(self, locationIds):
        self.setPresenceSomebodyInLocations(locationIds)
        return self

    def setPresenceSomebodyInLocations(self, locationIds, delay=DEFAULT_PRESENCE_DELAY):
        self.presence = BehaviourPresence().setLocationPresence(BehaviourPresenceType.somoneInLocation, locationIds,
                                                                delay)
        return self

    def setPresenceNobodyInLocations(self, locationIds, delay=DEFAULT_PRESENCE_DELAY):
        self.presence = BehaviourPresence().setLocationPresence(BehaviourPresenceType.nobodyInLocation, locationIds,
                                                                delay)
        return self

    def setNoEndCondition(self):
        self.endCondition = None
        return self

    def setEndConditionWhilePeopleInSphere(self):
        self.endCondition = BehaviourPresence().setSpherePresence(BehaviourPresenceType.someoneInSphere)
        return self

    def setEndConditionWhilePeopleInLocation(self, locationId):
        self.endCondition = BehaviourPresence().setLocationPresence(BehaviourPresenceType.somoneInLocation,
                                                                    [locationId])
        return self


class Twilight(BehaviourBase):

    def __init__(self, profileIndex=None, behaviourType=None, intensity=None, activeDays=None, time=None,
                 idOnCrownstone=None):
        super().__init__(profileIndex, behaviourType, intensity, activeDays, time, None, None, idOnCrownstone)

