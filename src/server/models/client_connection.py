from socket import SocketType
from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class ClientConnection:
    # todo: asignar un id a cada conexion, para poder identificarlas
    #       y pasarla a la app del cliente tambien mediante los comandos del server
    socket: SocketType
    address: tuple[str, int]

    def send_message(self, message: str) -> None:
        try:
            self.socket.send(message.encode('utf-8'))
        except Exception as e:
            raise ConnectionError(f'error sending message to client {self.address}: {e}')

    def receive_message(self) -> str:
        try:
            return self.socket.recv(1024).decode('utf-8')
        except Exception as e:
            raise ConnectionError(f'error receiving message from client {self.address}: {e}')

    def close(self):
        self.socket.close()

    def __str__(self):
        return f'{self.address[0]}:{self.address[1]}'
