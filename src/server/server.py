import socket as s
import ssl
import threading as t
import logging

from commons.interfaces import IEventListener

from .config import Config
from .models import ServerEvent as Event
from .application.connection_manager import ConnectionManager
from .models import ClientConnection


class Server(IEventListener):
    # TODO:
    #  - implementar un input en el server
    #     para introducir comandos desde ahi
    #  - validar que no se conecten mas clientes
    #     de los permitidos
    #       - actualizacion:
    #           el 3er cliente se conecta pero no envian sus mensajes: !!arreglar!!
    #  - implementar end-to-end encryption
    #  - implementar un sistema de autenticacion
    #  - procesar comandos de los clientes

    def __init__(self, host: str, port: int, max_conns: int):
        Config.setup_logging()

        self.host = host
        self.port = port
        self.max_conns = max_conns

        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain('certs/server.crt', 'certs/server.key')
        self.ssl_context = context

        self.socket_server = s.socket(s.AF_INET, s.SOCK_STREAM)

        self.running = False

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

            self.ssocket = self.ssl_context.wrap_socket(
                self.socket_server, server_side=True)

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
        self.ssocket.close()

    def accept_connections(self) -> None:
        logging.info('listening for incoming connections...')
        while self.running:
            try:
                # todo: buscar como conseguir la direccion, sin aceptar la conexion
                c_socket, c_addr = self.ssocket.accept()
                client = ClientConnection(socket=c_socket, address=c_addr)
                if len(self.connection_manager.clients) + 1 > self.max_conns:
                    self._reject_connection(client)
                    continue
                self.connection_manager.add_client(client)
                logging.info(
                    f'connection from {client} [{len(self.connection_manager.clients)}/{self.max_conns}]')

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
                    logging.debug(msg_log)
                else:
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
            logging.info(
                f'client at {client} removed [{len(self.connection_manager.clients)}/{self.max_conns}]')

    def _reject_connection(self, client: ClientConnection) -> None:
        logging.warning(
            f'connection from {client} rejected, maximum connections reached')
        self.server_command(f'reject {client}')

    def server_broadcast(self, message: str) -> None:
        self.connection_manager.broadcast(message.upper(), None)

    def server_command(self, command: str, *args) -> None:
        # todo: cambiar el nombre, no es tanto comandos lo que mando, como estados
        self.connection_manager.broadcast(
            f':command {command} {" ".join(args)}', None)

    def update(self, e: 'Event', d: str) -> None:
        self.server_broadcast(d)
