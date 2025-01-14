import sys

from .message_utils import MessageUtils


class AlertSystem:
    def __call__(self, *args, **kwargs):
        self.alert(*args, **kwargs)

    @staticmethod
    def alert(message: str, error: bool = False):
        if error:
            sys.stderr.write(MessageUtils.format_alerts(message, error))
            return
        sys.stdout.write(MessageUtils.format_alerts(message, error))
