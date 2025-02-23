class CommandProcessor:
    def __init__(self, client: "Client"):  # type: ignore
        self.client = client

    def process(self, command: str) -> bool:
        print('mi oppppppppppppp')  # todo: los comandos se estan procesando?
        args = command.split()
        if not args:
            return False

        if args[0] == 'shutdown':
            self.client.disconnect("Server requested shutdown")
            return True

        elif args[0] == 'reject':
            print(args)
            if str(args[1]) == str(self.client):
                self.client.disconnect("Server rejected connection")
                return True

        return False
