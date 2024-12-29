import sys
import socket as s
import threading as t
import readline as rl

from ..ansi import *


class Client:
    INPUT_PROMPT = '>> '
    INPUT_STRING = f'{YELLOW}{INPUT_PROMPT}{RESET}'
    RCV_PROMPT = f':: '
    count = 0

    def __init__(self, host='127.0.0.1', port=50000):
        self.host = host
        self.port = port
        self.socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.running: bool = False

    def start(self):
        SERVER_ADDR = (self.host, self.port)

        try:
            self.socket.connect(SERVER_ADDR)
            self.alert(f'connected to server at {self.host}:{self.port}')
            self.running = True
        except (ConnectionRefusedError, s.gaierror):
            self.alert(f'no server running at {self.host}:{self.port}', error=True)
            sys.exit(1)

        t.Thread(target=self.receive_messages, daemon=True).start()

        while self.running:
            try:
                if self.count != 0:
                    message: str = input(self.INPUT_STRING)
                else: # first message
                    message = input()
                    self.count += 1
                self.send_message(message)
            except OSError:
                break
            except KeyboardInterrupt:
                self.shutdown('user shutdown')
                break

    def shutdown(self, reason: str = 'unknown reason'):
        self.running = False
        self.alert(f'disconnecting from server: {reason}', error=True)
        self.socket.close()

    def send_message(self, message: str):
        try:
            self.socket.send(message.encode('utf-8'))
        except BrokenPipeError:
            self.alert(f'server has closed the connection', error=True)
            sys.exit(1)

    def receive_messages(self):
        # todo: estoy manejando tanto el input como la
        #   entraada de mensjaes, arreglar ese tema
        while self.running:
            try:
                raw_message = self.socket.recv(1024).decode('utf-8')

                if self.valid_command(raw_message):
                    if self.process_command(raw_message) != 1:
                        continue
                    break

                clean_message: str = self.normalize_message(raw_message)
                clean_line: callable[[str], str] = lambda msg: (
                    f'\r{" " * (len(msg) + len(self.INPUT_PROMPT))}\r'
                )
                ### mantener el input en la misma linea ###
                # coger el contenido del bufer
                current_input = rl.get_line_buffer()
                # limpiar la linea
                sys.stdout.write(clean_line(current_input))
                # output del mensaje
                msg_output = f'{CYAN}'
                if not self.is_srvr_msg(raw_message):
                    msg_output += f'{self.RCV_PROMPT}'
                msg_output += f'{clean_message}{RESET}\n'
                sys.stdout.write(msg_output)
                # poner el prompt de nuevo con lo escrito anteriormente
                # if current_input:
                sys.stdout.write(f'{self.INPUT_STRING}{current_input}')
                sys.stdout.flush()
                ############################################
            except OSError:
                break

    @staticmethod
    def normalize_message(message: str) -> str:
        return ' '.join(message.split()[1:])

    @staticmethod
    def is_srvr_msg(message: str) -> bool:
        return message.startswith('[SERVER]')

    @staticmethod
    def valid_command(message: str):
        return message.startswith('[SERVER] :command')

    def process_command(self, command: str) -> int:
        clean = lambda cmd, li: cmd.split()[li:]
        command = clean(command, 2)[0]
        # args = clean(command, 3)

        if command:
            if command == 'start':
                self.running = True
                self.start()
            elif command[0] == 'shutdown':
                self.shutdown('server shutdown')
                return 1
        return 0

    @staticmethod
    def alert(message: str, error: bool = False):
        message = f'\n=== {message.upper()} ===\n\n'
        if error:
            sys.stderr.write(f'{RED}{message}{RESET}')
        else:
            sys.stdout.write(f'{MAGENTA}{message}{RESET}')
