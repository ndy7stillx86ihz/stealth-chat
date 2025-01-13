import sys
import argparse

from .config import Config
from .server import Server

def main() -> int:
    parser = argparse.ArgumentParser(description='socket chat server')
    parser.add_argument(
        '-H', '--host',
        type=str,
        default=Config.HOST,
        help='host listening address'
    )
    parser.add_argument(
        '-p', '--port',
        type=int,
        default=Config.PORT,
        help='port listening address'
    )
    parser.add_argument(
        '-m', '--max-conns',
        type=int,
        default=Config.MAX_CONNS,
        help='maximum connections allowed'
    )

    try:
        args = parser.parse_args()
        MIN_PORT = 2 ** 10
        MAX_PORT = 2 ** 16 - 1
        if not MIN_PORT < args.port < MAX_PORT: #
            raise ValueError(f'port number must be between {MIN_PORT} and {MAX_PORT}')
        if args.max_conns < 2:
            raise ValueError('maxmimun number of connections must be 2 at least')
    except Exception as e:
        parser.error(str(e))

    server = Server(host=args.host, port=args.port, max_conns=args.max_conns)
    server.start()

    return 0

if __name__ == '__main__':
    sys.exit(main())
