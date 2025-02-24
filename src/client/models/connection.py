import socket
from ssl import SSLContext
import ssl

from .message import Message


class Connection:
    BUFFER_SIZE = 1024

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.server_address = (host, port)

        context = SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.check_hostname = False
        context.load_verify_locations(cafile="certs/server.crt")

        self.ssocket = context.wrap_socket(
            socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        )

        self.running = False

    def connect(self):
        self.ssocket.connect(self.server_address)
        self.running = True

    def disconnect(self):
        self.running = False
        self.ssocket.close()

    def send(self, message: 'Message'):
        self.ssocket.send(message.encode('utf-8'))

    def receive(self) -> 'Message':
        message = Message(self.ssocket.recv(self.BUFFER_SIZE).decode('utf-8'))
        return message
