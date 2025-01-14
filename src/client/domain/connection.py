import socket

from .message import Message

class Connection:
    BUFFER_SIZE = 1024

    def __init__(self, host: str, port: int):
        self.server_address = (host, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = False

    def connect(self):
        self.socket.connect(self.server_address)
        self.running = True

    def disconnect(self):
        self.running = False
        self.socket.close()

    def send(self, message: 'Message'):
        self.socket.send(message.encode('utf-8'))

    def receive(self) -> 'Message':
        message = Message(self.socket.recv(self.BUFFER_SIZE).decode('utf-8'))
        return message
