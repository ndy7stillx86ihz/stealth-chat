import sys
import readline

from ..utils import MessageUtils as Formatter


class Message(str):
    @property
    def is_command(self) -> bool:
        return self.startswith('[SERVER] :command')

    @property
    def is_broadcast(self) -> bool:
        return self.startswith('[SERVER]')

    def normalize(self) -> 'Message':
        return Message(' '.join(self.split()[1:]))

    def display(self) -> None:
        cleaned_msg = self.normalize()

        cleaned_line: callable[[str], str] = lambda msg: (
            f'\r{" " * (len(msg) + len(Formatter.INPUT_PROMPT_SYMBOL))}\r'
        )

        current_input = readline.get_line_buffer()

        sys.stdout.write(cleaned_line(current_input))
        sys.stdout.write(Formatter.format_received_message(cleaned_msg, self.is_broadcast))
        sys.stdout.write(f'{Formatter.INPUT_PROMPT}{current_input}')

        sys.stdout.flush()
