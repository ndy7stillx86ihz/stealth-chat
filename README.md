# CLI Socket Chat
   ![app-sample](sample/ui-example.png)


## Description

Project that using the **[socket](https://docs.python.org/3/library/socket.html)** library in **Python**, through the *client-server-client* model implements a minimalistic *CLI Chat*. The server is a module that can handle multiple clients at the same time using the multi-threading functionalities. It's able to broadcast messages, execute specific commands for event handling, for communicating with clients. Both clients can chat with each other freely, while the server handles the communication between them. 

## Installation and usage

### Setting up environment

#### **If you don't have [Poetry](https://python-poetry.org) installed:**

##### Linux, Mac-OS, WSL:

```sh
curl -sSL https://install.python-poetry.org | python3 -
```

##### Windows:

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

###### If you have installed Python through the Microsoft Store, replace `py` with `python` in the command above.

> Refer to [Poetry installation docs](https://python-poetry.org/docs/#installing-with-the-official-installer) for verifying, or getting more info

#### Install project dependencies

```bash
poetry install
```

##### **Now you should be able to run the main script:**

```sh
poetry run start --help  # to see script overview
```

### Server

#### To start the server, run the following command:

```bash
poetry run start server -p <port> -H <hostdir> -m <max-connections>
```


> **Be sure of setting up the server before trying to connect with client,  if not, you'll get an exception**

### Client

#### After someone hosts the server, enter the retrieved info

```bash
poetry run start client -p <server-port> -H <server-host>
```

> At first, you'll need to wait for the other peer to connect, you'll be able to send messages, but no one will receive them, whenever the peer sets up, the server will notify every client that there's at least one user to chat with.

## Known Issues

1. **Bad software design:** I'd rather to use a better architecture for more scalability, right now is a hell modifying anything because of the messy code

2. **Not encrypted messages:** Actually working on this issue

4. **Clients not being disconnected after closing server:** Sometimes after *KeyboardInterrumpting* the Server, the clients may just close as it's meant to be, but can also bug like receiving infinites messages.

   #### If you find any other Issue, please feel free to report it, or collaborating with the project :)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

