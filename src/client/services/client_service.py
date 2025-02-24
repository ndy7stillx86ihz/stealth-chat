import threading as t
from typing import Optional, Any

from client.infrastructure.command_processor import CommandProcessor
from client.models.client_event import ClientEvent
from client.models.connection import Connection
from client.models.message import Message
from client.presentation.message_renderer import MessageRenderer
from client.utils.alert_system import AlertSystem
from commons.abstracts import Event
from commons.interfaces.event_listener import IEventListener
from ..utils import MessageUtils
from ..models import Client
from .connection_service import ConnectionService


class ClientService(IEventListener):
    # todo: actualmente el cliente no sabe si el servidor
    #       le esta respondiendo, asi que debo poner algun sistema para parchear esto
    # todo: dar mejor salida cuando hay un connection refused, poner un mensaje mas amigable

    def __init__(self, client: Client):
        self.client = client
        self.connection_service = ConnectionService(
            Connection(client.host, client.port)
        )
        self.formatter = MessageUtils()
        self.command_processor = CommandProcessor(client)
        self.alert = AlertSystem()
        self.connection_service.publisher.subscribe(
            ClientEvent.CONNECTED_TO_SERVER,
            ClientEvent.CONNECTION_REFUSED,
            ClientEvent.DISCONNECTED_FROM_SERVER,
            ClientEvent.SERVER_DISCONNECTED,
            listener=self
        )
        self.input_counter = 0

    def start(self):
        self.connection_service.connect()

        # on an independent thread
        # start receiving messages
        t.Thread(target=self._receive_messages, daemon=True).start()

        # on main thread
        # start sending messages
        while self.connection_service.still_alive():
            try:
                prompt = self.formatter.format_input_prompt()
                message = Message(
                    input(prompt) if self.input_counter != 0 else input())
                self.input_counter += 1
                self.connection_service.send_message(message)
            except KeyboardInterrupt:
                self.shutdown("user requested shutdown")
                break

    def _receive_messages(self):
        while self.connection_service.connection.running:
            msg = Message(self.connection_service.receive_message())

            if not msg:
                break

            if msg.is_command:
                # print('es comando')
                if self.command_processor.process(msg):
                    break
                continue
            MessageRenderer.display(msg)

    def shutdown(self, reason: str = 'unknown reason'):
        self.connection_service.disconnect(reason)

    def update(self, e: Event, d: Optional[Any]) -> None:
        if d:
            self.alert(d)
