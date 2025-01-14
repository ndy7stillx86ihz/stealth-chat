import sys
import socket
from typing import Optional

from ..utils import AlertSystem
from ..domain import Message


class ConnectionService:
    from ..domain import Connection

    def __init__(self, connection: Connection):
        self.connection = connection

        self.alert = AlertSystem()

    def connect(self):
        try:
            self.connection.connect()

            self.alert(f"connected to server at {self.connection.server_address[0]}:{self.server_address[1]}")
            self.alert("press 'Enter' to start messaging")
            self.request_status()
        except (ConnectionRefusedError, socket.gaierror) as e:
            self.alert(message=f"connection refused: {e}", error=True)
            sys.exit(1)

    def disconnect(self, reason: str):
        self.alert(message=f"disconnecting from server: {reason}")
        self.connection.disconnect()

    def send_message(self, message: 'Message'):
        try:
            self.connection.send(message)
        except BrokenPipeError:
            self.alert("server has closed the connection")
            sys.exit(1)

    def receive_message(self) -> Optional['Message']:
        try:
            return self.connection.receive()
        except OSError:
            return None

    def request_status(self):
        pass
