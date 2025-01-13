import socket
import sys

from typing import Optional

from .alert_system import AlertSystem


class ConnectionHandler:
    BUFFER_SIZE = 1024

    def __init__(self, host: str, port: int):
        self.server_address = (host, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.alert = AlertSystem()
        self.running = False

    def connect(self):
        try:
            self.socket.connect(self.server_address)
            self.alert(f"connected to server at {self.server_address[0]}:{self.server_address[1]}")
            self.alert("press 'Enter' to start messaging")
            self.request_status()
            self.running = True
        except (ConnectionRefusedError, socket.gaierror) as e:
            self.alert(message=f"connection refused: {e}", error=True)
            sys.exit(1)

    def disconnect(self, reason: str):
        self.running = False
        self.alert(message=f"disconnecting from server: {reason}")
        self.socket.close()

    def send_message(self, message: str):
        try:
            self.socket.send(message.encode('utf-8'))
        except BrokenPipeError:
            self.alert("server has closed the connection")
            sys.exit(1)

    def receive_message(self) -> Optional[str]:
        try:
            return self.socket.recv(self.BUFFER_SIZE).decode('utf-8')
        except OSError:
            return None

    def request_status(self):
        # todo: implement request_status, envia un mensaje especial al server y maneja su respuesta
        pass

