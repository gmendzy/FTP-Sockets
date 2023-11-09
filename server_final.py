#!/usr/bin/env python3
import socket
import threading
import os

class ClientControlHandler(threading.Thread):
    def __init__(self, client_control_interface, address_port, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._client_control_interface = client_control_interface
        self._address_port = address_port

    def run(self):
        self._client_control_interface.handle_commands(self._address_port)


class FtpServer:
    def __init__(self, control_port):
        self.control_port = control_port

    def start(self):
        control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        control_socket.bind(("localhost", self.control_port))
        control_socket.listen(5) #server can have 5 pending connections at most to be accepted.
        print(f"FTP server is listening on port {self.control_port}")
        
        ongoing_threads = []
        while True:
            client_socket, address = control_socket.accept()
            print(f"Accepted connection from {address}")
            client_control_interface = FtpServerControlInterface(client_socket)
            client_control_handler = ClientControlHandler(client_control_interface, (address,), daemon=True)
            client_control_handler.start()
            ongoing_threads.append(client_control_handler)

            for ongoing_thread in ongoing_threads:
                if not ongoing_thread.is_alive():
                    ongoing_thread.join()

    


class FtpServerControlInterface:
    def __init__(self, control_socket):
        self.control_socket = control_socket

    def handle_commands(self, address: str):
        while True:
            command = self.control_socket.recv(1024).decode()
            if not command:
                break
            print(f"Server: Received command [{command}]")

            if command.startswith("put"):
                filename = command.split()[1]
                data_socket = self.data_connection()
                print("Listening...")
                data_socket, _ = data_socket.accept()
                print("Connected")
                self.put(data_socket)
            if command.startswith("get"):
                filename = command.split()[1]
                data_socket = self.data_connection()
                print("Listening...")
                data_socket, _ = data_socket.accept()
                print("Connected")
                self.get(data_socket, filename)
            if command.startswith("ls"):
                data_socket = self.data_connection()
                data_socket, _ = data_socket.accept()
                self.ls(data_socket)
            elif command == "quit":
                break
        print(f"Connection with {address} has been closed")
        self.control_socket.close()


    def data_connection(self): 
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_socket.bind(("localhost", 0)) # Ephermal port
        data_socket.listen(1)
        self.control_socket.send(str(data_socket.getsockname()[1]).encode())
        return data_socket
    
    def put(self, data_socket):
        print("Handling put...")
        with open("uploaded.txt", 'wb') as file:
            data = data_socket.recv(1024)
            while True:
                if not data:
                    break
                print(f"Received {len(data)}")
                file.write(data)
                data = data_socket.recv(1024)
            data_socket.close()
        print("File received successfully.")
    
    def get(self, data_socket, filename):
        print("Handling get...")
        full_path = os.path.join(os.getcwd(), filename)
        if os.path.isfile(full_path):
            with open(filename, 'rb') as file:
                data = file.read(1024)
                while data:
                    data_socket.send(data)
                    data = file.read(1024)
            data_socket.close()
        print("File sent successfully.")


    def ls(self, data_socket):
        files = os.listdir()
        file_list = "\n".join(files)
        data_socket.send(file_list.encode())
        data_socket.close()
        print("Directory list sent.")

if __name__ == "__main__":
    ftp_server = FtpServer(control_port  = 8080)
    ftp_server.start()


