from typing import Dict, List, Any
from ..interfaces import IEventListener

class EventManager:
    def __init__(self, *event_types: 'Event'):
        self.listeners: Dict['Event', List[IEventListener]] = {}
        for t in event_types:
            self.listeners[t] = []

    def subscribe(self, *event_types: 'Event', listener: IEventListener):
        for e in event_types:
            if e not in self.listeners:
                self.listeners[e] = []
            self.listeners[e].append(listener)

    def unsubscribe(self, event_type: 'Event', listener: IEventListener):
        self.listeners[event_type].remove(listener)

    def notify(self, event_type: 'Event', data: Any = None):
        for l in self.listeners[event_type]:
            l.update(data)
