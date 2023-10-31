import socket
import threading
import os


class FtpServer:
    def __init__(self, control_port):
        self.control_port = control_port

    def start(self):
        control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        control_socket.bind(("localhost", self.control_port))
        control_socket.listen(5) #server can have 5 pending connections at most to be accepted.
        print(f"FTP server is listening on port {self.control_port}")

        while True:
            client_socket, address = control_socket.accept()
            print(f"Accepted connection from {address}")
            client_control_interface = FtpServerControlInterface(client_socket)

            client_thread = threading.Thread(target=client_control_interface.handle_commands, args=(address,)) #creates a thread that executes client_control_interface.handle_commands, multiple client connections can be handled concurrently.
            client_thread.start()


class FtpServerControlInterface:
    def __init__(self, control_socket):
        self.control_socket = control_socket

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
            if command.startswith("get"):
                filename = command.split()[1]
                data_socket = self.data_connection()
                data_socket, _ = data_socket.accept()
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
        try:
            with open("received_file.txt", 'w') as file:
                data = data_socket.recv(1024)
                while data:
                    file.write(data)
                    data = data_socket.recv(1024)
                print("File received successfully.")
        except Exception as e:
                print(f"Error receiving file: {e}")
        finally:
            data_socket.close()
    
    def get(self, data_socket, filename):
        full_path = os.path.join(os.getcwd(), filename)
        if os.path.isfile(full_path):
            with open("sent_file.txt", 'r') as file:
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


