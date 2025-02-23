class Message(str):
    @property
    def is_command(self) -> bool:
        return self.startswith('[SERVER] :command')

    @property
    def is_broadcast(self) -> bool:
        return self.startswith('[SERVER]')

    def normalize(self) -> 'Message':
        return Message(' '.join(self.split()[1:]))
