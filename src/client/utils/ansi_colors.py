from enum import Enum


class ANSI(Enum):
    """
    the content of this enum is a partial copypaste from my Gist:
       https://gist.github.com/duckraper/c28c430accf041736463f47c9c370fd9
    """
    RESET = '\033[0m'

    YELLOW = '\033[33m'
    RED = '\033[31m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    ORANGE = '\033[38;5;214m'  # server broadcast

    def __str__(self):
        return self.value
