import threading as t

from client.application.command_processor import CommandProcessor
from client.domain.connection import Connection
from ..application.connection_service import ConnectionService
from ..utils import MessageUtils
from .message import Message


class Client:
    def __init__(self, host: str = '127.0.0.1', port: int = 50000):
        self.connection = ConnectionService(host, port)
        # self.formatter = MessageUtils()
        # self.command_processor = CommandProcessor(self)
        self.input_count = 0
        
    def connect(self) -> None:
        self.connection.connect()

    def disconnect(self, reason):
        self.connection.disconnect(reason)

    def _receive_messages(self):
        while self.connection.running:
            msg = Message(self.connection.receive())

            if not msg:
                break

            if msg.is_command:
                # print('es comando')
                if self.command_processor.process(msg):
                    break
                continue
            msg.display()

    def __str__(self):
        return f'{self.connection.server_address[0]}:{self.connection.server_address[1]}'
