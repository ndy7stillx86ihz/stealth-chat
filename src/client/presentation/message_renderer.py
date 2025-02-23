import sys
import readline

from ..utils import MessageUtils


class MessageRenderer:
    from ..models import Message

    @staticmethod
    def display(message: 'Message') -> None:
        """output messages and avoids input overlapping"""
        cleaned_msg = message.normalize()

        cleaned_line: callable[[str], str] = lambda msg: ( # type: ignore
            f'\r{" " * (len(msg) + len(MessageUtils.INPUT_PROMPT_SYMBOL))}\r'
        )

        current_input = readline.get_line_buffer()

        sys.stdout.write(cleaned_line(current_input))
        sys.stdout.write(MessageUtils.format_received_message(cleaned_msg, message.is_broadcast))
        sys.stdout.write(f'{MessageUtils.INPUT_PROMPT}{current_input}')

        sys.stdout.flush()
