import socket
import os
from enum import Enum
import threading

class FtpServerCommand(Enum):
    GET = "get"
    PUT = "put"
    LS = "ls"

class FtpServerControlInterface:
    def __init__(self, control_socket, data_port):
        self.control_socket = control_socket
        self.data_port = data_port
    
    def handle_commands(self, address):
        while True:
            command = self.control_socket.recv(1024).decode()
            if not command:
                break

            if command.startswith(FtpServerCommand.GET.value):
                filename = command.split()[1]
                data_socket = self.setup_data_connection()
                self.send_file(data_socket, filename)
            elif command.startswith(FtpServerCommand.PUT.value):
                filename = command.split()[1]
                data_socket = self.setup_data_connection()
                self.receive_file(data_socket, filename)
            elif command.startswith(FtpServerCommand.LS.value):
                data_socket = self.setup_data_connection()
                self.list_files(data_socket)
            elif command == "quit":
                break
        self.control_socket.close()
        print("Connection with {} closed.".format(address))

    def setup_data_connection(self):
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_socket.bind(("localhost", self.data_port))
        data_socket.listen(1)
        self.control_socket.send(str(self.data_port).encode())
        return data_socket
    

    def send_file(self):
        if os.path.isfile(self.filename):
            with open(self.filename, "rb") as file:
                data = file.read(1024)
                while data:
                    self.data_socket.send(data)
                    data = file.read(1024)
        self.data_socket.close()

    def receive_file(self):
        with open(self.filename, "wb") as file:
            data = self.data_socket.recv(1024)
            while data:
                file.write(data)
                data = self.data_socket.recv(1024)
            self.data_socket.close()
        print("File received successfully")

    def list_files(self):
        files = os.listdir()
        file_list = "\n".join(files)
        self.data_socket.send(file_list.encode())
        self.data_socket.close()


class FtpServer:
    def __init__(self, control_port, data_port):
        self.control_port = control_port
        self.data_port = data_port

    def start(self):
        control_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        control_server_socket.bind(("localhost", self.control_port))
        control_server_socket.listen(5)
        print("FTP control server is listening on port {}".format(self.data_port))

        while True:
            client_control_socket, address = control_server_socket.accept()
            print("Accepted connection from {}".format(address))
            client_control_interface = FtpServerControlInterface(client_control_socket, self.data_port)

            client_thread = threading.Thread(target = client_control_interface.handle_commands, args = (address,))
            client_thread.start()


if __name__ == "__main__":
    ftp_server = FtpServer(control_port = 8080, data_port=8181)
    ftp_server.start()
