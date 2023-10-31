import socket
import threading
from enum import Enum


class FtpServerCommand(Enum):
    GET = "get"
    PUT = "put"
    LS = "ls"

class FtpClient:
    def __init__(self):
        self.addr = "localhost"
        self.port = 8080
        

    
    def start(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.addr, self.port))
        
        while True:
            command = input("ftp> ")
            client_socket.send(command.encode())
            if command == "quit":
                break

            if command.startswith(FtpServerCommand.PUT.value) or \
               command.startswith(FtpServerCommand.GET.value): 
                self.data_port = int(client_socket.recv(1024).decode())
                data_socket = self.data_connection()
                filename = command.split()[1]
            if command.startswith(FtpServerCommand.LS.value):
                self.data_port = int(client_socket.recv(1024).decode())
                data_socket = self.data_connection()
                if command.startswith(FtpServerCommand.PUT.value):
                    self.perform_put(data_socket, filename)
                elif command.startswith(FtpServerCommand.GET.value):
                    self.perform_get(data_socket, filename)
                elif command.startswith(FtpServerCommand.LS.value):
                    self.perform_ls(data_socket)

        
        client_socket.close()

    def data_connection(self):
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_socket.connect((self.addr, self.data_port))
        return data_socket


     
    def perform_put(self, data_socket, filename):
        with open(filename, 'r') as file:
            data = file.read(1024)
            while data:
                data_socket.send(data)
                data = file.read(1024)
            data_socket.close()
        print("File sent successfully.")

    def perform_get(self, data_socket):
        with open("new_file", 'w') as file:
            data = data_socket.recv(1024)
            while data:
                file.write(data)
                data = data_socket.recv(1024)
            data_socket.close()
        print("File received successfully.")

    def perform_ls(self, data_socket):
        directory_list = data_socket.recv(1024).decode()
        print("Directory List: ")
        print(directory_list)
        data_socket.close()

    

if __name__ == "__main__":
    ftp_client = FtpClient()
    ftp_client.start()
