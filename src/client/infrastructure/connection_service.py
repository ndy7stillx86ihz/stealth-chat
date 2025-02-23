import sys
import socket
from typing import Optional

from client.models.client_event import ClientEvent
from commons.services.event_manager import EventManager

from ..models import Message


class ConnectionService:
    from ..models import Connection

    def __init__(self, connection: Connection):
        self.connection = connection
        self.publisher = EventManager()

    def connect(self):
        try:
            self.connection.connect()
            self.publisher.notify(ClientEvent.CONNECTED_TO_SERVER)

            self.request_status()
        except (ConnectionRefusedError, socket.gaierror) as e:
            self.publisher.notify(ClientEvent.CONNECTION_REFUSED,
                                  f"{str(e)}, no server found at {self.connection.host}:{self.connection.port}")
            sys.exit(1)

    def disconnect(self, reason: str):
        self.publisher.notify(ClientEvent.DISCONNECTED_FROM_SERVER, reason)
        self.connection.disconnect()

    def send_message(self, message: 'Message'):
        try:
            self.connection.send(message)
        except BrokenPipeError:
            self.publisher.notify(ClientEvent.SERVER_DISCONNECTED)
            sys.exit(1)

    def receive_message(self) -> Optional['Message']:
        try:
            return self.connection.receive()
        except OSError:
            return None

    def still_alive(self) -> bool:
        return self.connection.running

    def request_status(self):
        pass
