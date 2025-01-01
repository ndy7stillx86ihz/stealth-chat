import socket as s
import threading as t
import logging

from ..config import Config
from .enums import Event
from .interfaces import IEventListener
from .managers.connection_manager import ConnectionManager
from .models import ClientConnection


class Server(IEventListener):
    # TODO:
    #  - implementar un input en el server
    #     para introducir comandos desde ahi
    #  - validar que no se conecten mas clientes
    #     de los permitidos
    #  - implementar end-to-end encryption
    #  - implementar un sistema de autenticacion

    def __init__(self, host: str, port: int, max_conns: int):
        Config.setup_logging()

        self.host = host
        self.port = port
        self.max_conns = max_conns
        self.running = False
        self.socket_server = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.connection_manager = ConnectionManager()
        self.connection_manager.publisher.subscribe(
            Event.CLIENT_DISCONNECTED,
            Event.CLIENT_REMOVED,
            Event.CLIENT_CONNECTED,
            Event.CLIENT_RECONNECTED,
            listener=self
        )

    def start(self):
        try:
            BINDING_ADDR = (self.host, self.port)

            self.socket_server.bind(BINDING_ADDR)
            self.socket_server.listen()
            self.running = True
            logging.info(f'server started at {self.host}:{self.port}')
            self.accept_connections()

        except Exception as e:
            logging.error(f'error starting server: {e}')
        finally:
            self.shutdown()

    def shutdown(self) -> None:
        logging.info('shutting down server...')
        
        self.server_broadcast('server shutdown, goodbye!')
        self.server_command('shutdown')
        self.running = False
        self.socket_server.close()

    def accept_connections(self) -> None:
        logging.info('listening for incoming connections...')
        while self.running:
            try:
                c_socket, c_addr = self.socket_server.accept()
                client = ClientConnection(socket=c_socket, address=c_addr)
                self.connection_manager.add_client(client)
                logging.info(f'connection from {client} [{len(self.connection_manager.clients)}/{self.max_conns}]')

                t.Thread(
                    name=f'thread-{client}',
                    target=self.handle_client,
                    args=(client,),
                    daemon=True
                ).start()

            except s.timeout:
                continue
            except KeyboardInterrupt:
                break
            except Exception as e:
                logging.error(f'error handling connections: {e}')

    def handle_client(self, client: ClientConnection) -> None:
        logging.info(f'handling client {client}')
        try:
            while self.running:
                message = client.receive_message()
                if not message:
                    break

                msg_log = f'message from {client}'
                if Config.DEBUG:
                    msg_log += f': \'{message}\''
                logging.info(msg_log)

                self.connection_manager.broadcast(message, client)
        except ConnectionError as e:
            logging.warning(e)
        except (ConnectionResetError, s.error):
            logging.warning(f'client at {client} unexpectedly disconnected')
        except Exception as e:
            logging.error(f'error handling client {client}: {e}')
        finally:
            self.connection_manager.remove_client(client)
            logging.info(f'client at {client} removed [{len(self.connection_manager.clients)}/{self.max_conns}]')

    def server_broadcast(self, message: str) -> None:
        self.connection_manager.broadcast(
            f'\n\033[38;5;214m### {message.upper()} ###\033[0m\n', None)

    def server_command(self, command: str, *args) -> None:
        self.connection_manager.broadcast(
            f':command {command} {" ".join(args)}', None)

    def update(self, d: str) -> None:
        self.server_broadcast(d)
