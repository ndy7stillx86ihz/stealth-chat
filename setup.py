import subprocess
import argparse
import sys

def run_module(module, host, port, max_conns=None):
    command = ['python3', '-m', f'src.{module}', '--host', host, '--port', str(port)]
    if module == 'server' and max_conns is not None:
        command.extend(['--max-conns', str(max_conns)])
    subprocess.run(command)

def main():
    parser = argparse.ArgumentParser(description='Run client or server module')
    parser.add_argument('module', choices=['client', 'server'], help='Module to run')
    parser.add_argument('--host', '-H', type=str, default='127.0.0.1', help='Host address')
    parser.add_argument('--port', '-p', type=int, default=50000, help='Port number')
    parser.add_argument('--max-conns', '-m', default=2, type=int, help='Maximum connections (server only)')

    args = parser.parse_args()

    if args.module == 'server' and args.max_conns is None:
        parser.error('The --max-conns argument is required for the server module')

    run_module(args.module, args.host, args.port, args.max_conns)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        print('\nquitting...')
    finally:
        sys.exit(0)
