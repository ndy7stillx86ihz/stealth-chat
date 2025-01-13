import sys
import argparse
from .client import Client

def main() -> int:
    parser = argparse.ArgumentParser(description='socket chat client')
    parser.add_argument('--host', '-H', type=str, default='127.0.0.1', help='server address')
    parser.add_argument('--port', '-p', type=int, default=50000, help='server port')

    try:
        args = parser.parse_args()
        MIN_PORT = 2 ** 10
        MAX_PORT = 2 ** 16 - 1
        if not MIN_PORT < args.port < MAX_PORT: #
            raise ValueError(f'port number must be between {MIN_PORT} and {MAX_PORT}')
    except Exception as e:
        parser.error(str(e))

    client = Client(host=args.host, port=args.port)
    client.start()

    return 0

if __name__ == '__main__':
    sys.exit(main())
