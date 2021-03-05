import uuid
from typing import Callable, Any

class EventBus:

    def __init__(self):
        self.topics = {}
        self.subscriberIds = {}


    def once(self, topic: str, callback: Callable[[Any], None]):
        def cleanup(bus, subId, data):
            bus.unsubscribe(subId)
            callback(data)

        subscriptionId = self.subscribe(topic, lambda data: cleanup(self, subscriptionId, data))

    def subscribe(self, topic: str, callback: Callable[[Any], None]) -> str:
        if topic not in self.topics:
            self.topics[topic] = {}

        subscriptionId = str(uuid.uuid4())
        self.subscriberIds[subscriptionId] = topic
        self.topics[topic][subscriptionId] = callback

        return subscriptionId

    def emit(self, topic: str, data: Any = True):
        if topic in self.topics:
            callbackIds = list(self.topics[topic].keys())
            for subscriptionId in callbackIds:
                self.topics[topic][subscriptionId](data)


    def unsubscribe(self, subscriptionId: str):
        if subscriptionId is None:
            return

        if subscriptionId in self.subscriberIds:
            topic = self.subscriberIds[subscriptionId]
            if topic in self.topics:
                self.topics[topic].pop(subscriptionId)

            self.subscriberIds.pop(subscriptionId)
        else:
            pass
            #print("ERROR: BluenetEventBus: Subscription ID ", subscriptionId, " cannot be found.")

