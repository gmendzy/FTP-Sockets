#!/usr/bin/env python3
import socket
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
        while True:
            try:
                command = input("ftp> ")
                print(f"Client: Received command [{command}]")
            except EOFError:
                break
            if command == "quit" or not command:
                break

            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.addr, self.port))
            client_socket.send(command.encode())
            
            if command.startswith(FtpServerCommand.PUT.value):
                filename = command.split()[1]
                self.data_port = int(client_socket.recv(1024).decode())
                data_socket = self.data_connection()
                self.perform_put(data_socket, filename)
            if command.startswith(FtpServerCommand.GET.value):
                filename = command.split()[1]
                self.data_port = int(client_socket.recv(1024).decode())
                data_socket = self.data_connection()
                self.perform_get(data_socket)
            if command.startswith(FtpServerCommand.LS.value):
                self.data_port = int(client_socket.recv(1024).decode())
                data_socket = self.data_connection()
                self.perform_ls(data_socket)
            

        
        client_socket.close()

    def data_connection(self):
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_socket.connect((self.addr, self.data_port))
        return data_socket


     
    def perform_put(self, data_socket, filename):
        print(f"Client: Sending {filename}")
        with open(filename, 'rb') as file:
            data = file.read(1024)
            while True:
                if not data:
                    break
                print(f"Client: Sending {len(data)} bytes of data.")
                data_socket.send(data)
                data = file.read(1024)
                print("Client: File sent successfully.")
            data_socket.close()
  



    
    def perform_get(self, data_socket):
        print(f"Client: Receiving file...")
        with open("downloaded.txt", 'wb') as file:
            data = data_socket.recv(1024)
            while data:
                file.write(data)
                print(f"Client: Received {len(data)} bytes of data.")
                data = data_socket.recv(1024)
                print("Client: File received successfully.")
            data_socket.close()
        

    
    def perform_ls(self, data_socket):
        directory_list = data_socket.recv(1024).decode()
        print("Directory List: ")
        print(directory_list)
        data_socket.close()

    

if __name__ == "__main__":
    ftp_client = FtpClient()
    ftp_client.start()
