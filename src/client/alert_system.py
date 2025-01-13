import sys

from .message_formatter import MessageFormatter


class AlertSystem:
    def __call__(self, *args, **kwargs):
        self.alert(*args, **kwargs)

    @staticmethod
    def alert(message: str, error: bool = False):
        if error:
            sys.stderr.write(MessageFormatter.format_alerts(message, error))
            return
        sys.stdout.write(MessageFormatter.format_alerts(message, error))
