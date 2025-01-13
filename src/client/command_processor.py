class CommandProcessor:
    def __init__(self, client: "Client"):
        self.client = client

    def process(self, command: str) -> bool:
        print('mi pingaaa')
        args = command.split()
        if not args:
            return False

        if args[0] == 'shutdown':
            self.client.shutdown("Server requested shutdown")
            return True

        elif args[0] == 'reject':
            print(args)
            if str(args[1]) == str(self.client):
                self.client.shutdown("Server rejected connection")
                return True

        return False
