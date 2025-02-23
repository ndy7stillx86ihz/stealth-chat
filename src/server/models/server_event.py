from commons.abstracts.event import Event


class ServerEvent(Event):
    CLIENT_REMOVED = 1
    CLIENT_CONNECTED = 2
    FULL_SERVER = 3
    CLIENT_DISCONNECTED = 4
    CLIENT_RECONNECTED = 5
