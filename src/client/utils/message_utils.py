from .ansi_colors import ANSI


class MessageUtils:
    INPUT_PROMPT_SYMBOL = '>> '
    RECEIVED_PROMPT_SYMBOL = '::'
    INPUT_PROMPT = f"{ANSI.YELLOW}{INPUT_PROMPT_SYMBOL}{ANSI.RESET}"
    RECEIVED_PROMPT = f"{ANSI.CYAN}{RECEIVED_PROMPT_SYMBOL}{ANSI.RESET}"

    @staticmethod
    def format_input_prompt() -> str:
        return f"{ANSI.YELLOW}>> {ANSI.RESET}"

    @staticmethod
    def format_received_message(message: str, is_server: bool) -> str:
        # todo: al formatear mal no se estan procesando bien los mensajes, fix!
        prompt_prefix = ":: " if not is_server else "### "
        prompt_suffix = "" if not is_server else " ###"
        color = ANSI.CYAN if not is_server else ANSI.ORANGE

        return f"{color}{prompt_prefix}{message}{prompt_suffix}{ANSI.RESET}\n"

    @staticmethod
    def format_alerts(message: str, error: bool) -> str:
        symbol = '---' if error else '+++'
        prefix = ANSI.RED if error else ANSI.MAGENTA
        return f"{prefix}{symbol} {message.upper()} {symbol}{ANSI.RESET}\n"
