# Group Members:
* Geoff Mendoza : mendoza.geoff@csu.fullerton.edu
* Wesley Zoroya

## Simple FTP Server and Client using TCP Sockets
This is a basic implementation of a File Transfer Protocol (FTP) server and client using the Transmission Control Protocol (TCP). The server and client are designed to run on the same machine and allow you to upload (put) and download (get) files to and from the server.

# How it Works
* The FTP system consists of two main components: the server and the client.

# FTP Server
* The FTP server is responsible for listening to incoming connections from clients and handling file transfers. Here's how it works:

* The server listens on a specified control port (by default, port 8080) for incoming client connections.
* When a client connects, the server accepts the connection and creates a control socket to communicate with the client.
* The client can issue several commands to the server, including put, get, and ls (list files in the server's directory).
* For data transfer (file upload or download), the server establishes a separate data connection, allowing the client to send or receive files.
* The server can handle multiple clients simultaneously using multi-threading, allowing several clients to connect and transfer files concurrently.
# FTP Client
* The FTP client is used to connect to the server and issue commands for file transfers. Here's how it works:

* The client connects to the server's control port (by default, port 8080) to establish a control channel.
* The client can input commands such as put, get, ls, and quit. The put and get commands are used to upload and download files, respectively.
* When a put or get command is issued, the server responds with an ephemeral port number for the data connection.
* The client then establishes a data connection with the server on the provided ephemeral port for file transfer.
* After the file transfer is complete, the data connection is closed.

#  Server

The server listens for incoming connections on port 8080 by default. You can change this port as needed.

Example usage:

```sh
chmod +x server_final.py
./server_final.py
```

# Client

You can use commands like put, get, ls, and quit to interact with the server. When using put or get, the client will prompt you for a filename.

Example usage:

```sh
chmod +x client_final.py

# To list
printf "ls\n" | ./client_final.py

# To upload
printf "put upload_this.txt\n" | ./client_final.py

# To download
printf "get file_from_server.txt\n" | ./client_final.py
```

# Dependencies
This implementation uses Python's built-in socket, os, threading, and enum modules. No external libraries are required.

