import socket
import os

class FtpServer:
    def __init__(self, control_port):
        self.control_port = control_port
        self.data_socket = None

    def start(self):
        control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        control_socket.bind(("localhost", self.control_port))
        control_socket.listen(5)
        print(f"FTP server is listening on port {self.control_port}")

        while True:
            client_socket, address = control_socket.accept()
            print(f"Accepted connection from {address}")
            client_control_interface = FtpServerControlInterface(client_socket, self)

            client_control_interface.handle_commands(address)

class FtpServerControlInterface:
    def __init__(self, control_socket, server):
        self.control_socket = control_socket
        self.server = server

    def handle_commands(self, address):
        while True:
            command = self.control_socket.recv(1024).decode()
            if not command:
                break

            if command.startswith("put"):
                filename = command.split()[1]
                data_socket = self.data_connection()
                data_socket, _ = data_socket.accept()
                self.put(data_socket)
            elif command == "quit":
                break

        print(f"Connection with {address} has been closed")
        self.control_socket.close()

    def data_connection(self):
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_socket.bind(("localhost", 0))  # Ephemeral port
        data_socket.listen(1)
        self.control_socket.send(str(data_socket.getsockname()[1]).encode())
        return data_socket

    def put(self, data_socket):
        with open("received_file.txt", 'wb') as file:
            data = data_socket.recv(1024)
            while data:
                file.write(data)
                data = data_socket.recv(1024)
            data_socket.close()
        print("File received successfully.")

if __name__ == "__main__":
    ftp_server = FtpServer(control_port=8080)
    ftp_server.start()
