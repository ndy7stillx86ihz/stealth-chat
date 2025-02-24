from .models import Client
from .services.client_service import ClientService


class ClientApp:
    def __init__(self, host: str, port: int):
        self.client = ClientService(Client(host, port))

    def start(self):
        self.client.start()
