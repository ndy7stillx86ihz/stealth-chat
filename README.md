# CLI Socket Based Chat
   ![app-sample](sample/image-20241229034504006.png)


## Description

Implementation of a chat using the [socket](https://docs.python.org/3/library/socket.html) library in Python using  the client-server-client model. The server is a multithreaded server that can handle multiple clients at the same time. It  is able to broadcast messages, execute specific commands for event handling, for communicating with clients. Both clients can chat with each other freely, while the server handles the communication between them. 

## Usage

### Server

#### To start the server, run the following command:

```bash
python setup.py server -p <port> -H <hostdir> -m <max-connections>
```

###### 		  Or replace `python setup.py` with `./setup` and keep the same arguments as above.

> **Be sure of setting up the server before trying to connect with client,  if not, you'll get an exception**

### Client

#### After setting up the server, enter the same arguments for connecting with the client

```bash
python setup.py client -p <server-port> -H <server-host>
```

###### As before you can also use the `./setup` binary instead of using python directly

#### At first, you'll need to wait for the other peer to connect, you'll be able to send messages, but no one will receive them, whenever the peer sets up the server will notify every client  there's at least one to chat with.

### Known Issues

1. **Bad software design:** I'd rather to use a better architecture for more scalability, right now is a hell modifying anything because of  the messy code

2. **Not encrypted messages:** It's my next goal for the project

3. **Poor Exceptions handling** 

4. **Clients not being disconnected after closing server:** Sometimes after *KeyboardInterrumpting* the Server, the clients may just close as it's meant to be, but can also bug like receiving infinites messages.

   #### If you find any other Issue, please feel free to report it, or collaborating with the project :)

