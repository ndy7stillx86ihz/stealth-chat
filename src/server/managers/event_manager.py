from typing import Dict, List, Any
from ..interfaces import IEventListener

class EventManager:
    def __init__(self, *event_types: int):
        self.listeners: Dict[int, List[IEventListener]] = {}
        for t in event_types:
            self.listeners[t] = []

    def subscribe(self, *event_types: int, listener: IEventListener):
        for e in event_types:
            if e not in self.listeners:
                self.listeners[e] = []
            self.listeners[e].append(listener)

    def unsubscribe(self, event_type: int, listener: IEventListener):
        self.listeners[event_type].remove(listener)

    def notify(self, event_type: int, data: Any = None):
        for l in self.listeners[event_type]:
            l.update(data)
