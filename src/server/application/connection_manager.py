from threading import Lock
from typing import Optional, List

from ..models import ClientConnection, ServerEvent as Event
from commons.services.event_manager import EventManager


class ConnectionManager:
    def __init__(self):
        self.clients: List[ClientConnection] = []
        self.lock = Lock()
        self.publisher = EventManager(
            Event.CLIENT_DISCONNECTED,
            Event.CLIENT_REMOVED,
            Event.CLIENT_CONNECTED,
            Event.CLIENT_RECONNECTED
        )

    def add_client(self, client: ClientConnection):
        with self.lock:
            self.clients.append(client)
            if len(self.clients) > 1:
                self.publisher.notify(
                    Event.CLIENT_CONNECTED, 'peer connected to chat')

    def remove_client(self, client: ClientConnection):
        with self.lock:
            self.clients.remove(client)
            client.close()
            self.publisher.notify(Event.CLIENT_DISCONNECTED,
                                  'peer disconnected from chat')

    def broadcast(self, message: str, sender: Optional[ClientConnection] = None):
        # with self.lock:
        # todo: arreglar esto
        disconnected_clients: List[ClientConnection] = []
        for client in self.clients:
            if client != sender:
                try:
                    prefix = '[SERVER]' if sender is None else '[CLIENT]'
                    client.send_message(prefix + ' ' + message)
                except ConnectionError as e:
                    disconnected_clients.append(client)
                    raise ConnectionError(e)

        for client in disconnected_clients:
            self.remove_client(client)
