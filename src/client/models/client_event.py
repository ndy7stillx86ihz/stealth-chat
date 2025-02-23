from commons.abstracts import Event


class ClientEvent(Event):
    CONNECTED_TO_SERVER = 1
    DISCONNECTED_FROM_SERVER = 2
    CONNECTION_REFUSED = 3
    SERVER_DISCONNECTED = 4
    
