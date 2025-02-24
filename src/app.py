import argparse
import sys
from importlib import import_module


def run_module(module, host, port, max_conns=None):
    original_argv = sys.argv.copy()
    try:
        args_list = [module, '--host', host, '--port', str(port)]
        if module == 'server' and max_conns is not None:
            args_list.extend(['--max-conns', str(max_conns)])

        sys.argv = args_list

        module_main = import_module(f"{module}.__main__").main

        try:
            module_main()
        except KeyboardInterrupt:
            sys.exit(0)
    finally:
        sys.argv = original_argv  # Restaura sys.argv


def main():
    parser = argparse.ArgumentParser(description='Run client or server module')
    parser.add_argument('module', choices=[
                        'client', 'server'], help='Module to run')
    parser.add_argument('--host', '-H', type=str,
                        default='127.0.0.1', help='Host address')
    parser.add_argument('--port', '-p', type=int,
                        default=50000, help='Port number')
    parser.add_argument('--max-conns', '-m', type=int,
                        default=2, help='Maximum connections (server only)')

    args = parser.parse_args()

    if args.module == 'server' and args.max_conns is None:
        parser.error(
            'The --max-conns argument is required for the server module')

    run_module(args.module, args.host, args.port, args.max_conns)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
