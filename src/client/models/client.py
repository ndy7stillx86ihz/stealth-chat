from typing import Self


class Client:
    ID = 0

    def __new__(cls, *args, **kwargs) -> Self:
        cls.ID += 1
        return super().__new__(cls)

    def __init__(self, host: str = '127.0.0.1', port: int = 50000):
        self.host = host
        self.port = port
        self.input_count = 0

    def __str__(self):
        return f'{self.host}:{self.port}'
