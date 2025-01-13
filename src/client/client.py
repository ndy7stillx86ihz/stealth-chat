import sys
import socket as s
import threading as t

from .command_processor import CommandProcessor
from .connection_handler import ConnectionHandler
from .message_formatter import MessageFormatter
from .message_model import Message


class Client:
    # todo: actualmente el cliente no sabe si el servidor
    #       le esta respondiendo, asi que debo poner algun sistema para parchear esto
    def __init__(self, host='127.0.0.1', port=50000):
        self.connection = ConnectionHandler(host, port)
        self.formatter = MessageFormatter()
        self.command_processor = CommandProcessor(self)
        self.input_count = 0

    def start(self):
        self.connection.connect()
        t.Thread(target=self._receive_messages, daemon=True).start()

        while self.connection.running:
            try:
                prompt = self.formatter.format_input_prompt()
                message = input(prompt) if self.input_count != 0 else input()
                self.input_count += 1
                self.connection.send_message(message)
            except KeyboardInterrupt:
                self.shutdown("user requested shutdown")
                break

    def shutdown(self, reason: str = 'unknown reason'):
        self.connection.disconnect(reason)

    def _receive_messages(self):
        while self.connection.running:
            msg = Message(self.connection.receive_message())

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
