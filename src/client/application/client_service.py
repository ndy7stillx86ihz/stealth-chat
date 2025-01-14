import threading as t

from client.application.command_processor import CommandProcessor
from client.domain.connection import Connection
from ..utils import MessageUtils
from ..domain import Client
from .connection_service import ConnectionService

class ClientService:
    # todo: actualmente el cliente no sabe si el servidor
    #       le esta respondiendo, asi que debo poner algun sistema para parchear esto

    def __init__(self, client: Client):
        self.client = client
        self.connection_service = ConnectionService(client.connection)
        self.command_processor = CommandProcessor()
        self.input_counter = 0

    def start(self):
        self.client.connect()

        t.Thread(target=self._receive_messages, daemon=True).start()

        while self.connection.running:
            try:
                prompt = self.formatter.format_input_prompt()
                message = Message(input(prompt) if self.input_count != 0 else input())
                self.input_count += 1
                self.connection.send(message)
            except KeyboardInterrupt:
                self.shutdown("user requested shutdown")
                break

    def shutdown(self, reason : str = 'unknown reason'):
        self.client.disconnect(reason)


