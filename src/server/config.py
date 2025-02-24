import logging

from rich.logging import RichHandler


class Config:
    HOST = '0.0.0.0'
    PORT = 50000
    MAX_CONNS = 2
    DEBUG = True

    @staticmethod
    def setup_logging():
        logging.basicConfig(
            format='%(asctime)s - %(levelname)s - %(message)s',
            level=logging.DEBUG if Config.DEBUG else logging.INFO,
            handlers=[RichHandler(
                omit_repeated_times=False,
                show_path=False,
                rich_tracebacks=True
            )]
        )
