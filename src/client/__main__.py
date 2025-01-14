import sys
import argparse
from .domain import Client

def main() -> int:
    parser = argparse.ArgumentParser(description='socket chat client')
    parser.add_argument('--host', '-H', type=str, default='127.0.0.1', help='server address')
    parser.add_argument('--port', '-p', type=int, default=50000, help='server port')

    try:
        args = parser.parse_args()
        min_port = 2 ** 10  # 1024
        max_port = 2 ** 16 - 1  # 65535
        if not min_port < args.port < max_port:
            raise ValueError(f'port number must be between {min_port} and {max_port}')
    except Exception as e:
        parser.error(str(e))

    client = Client(host=args.host, port=args.port)
    client.start()

    return 0


if __name__ == '__main__':
    sys.exit(main())
