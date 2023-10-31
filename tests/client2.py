from enum import Enum
import socket
import sys

class FtpServerCommand(Enum):
    GET = "get"
    PUT = "put"
    LS = "ls"

class FtpServerControlInterface:
    def __init__(self):
        self.control_channel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def connect(self, addr: str, port: int) -> bool:
        try:
            self.sock.connect((addr, port))
            return True
        except Exception as e:
            print("Connection error: {}".format(e))
            return False
    
    def command(self, command: str) -> bool:
            self._socket.send(command.encode())
            response = self.sock.recv(1024).decode()
            return self._handle_response(response)
        
    def _handle_response(response: str) -> bool:
        return response == "OK"


class FtpServerDataInterface:
    def __init__(self):
        self.data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect(self, addr: str, port: int) -> bool:
        try:
            self.data_socket.connect((addr, port))
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False

    
    def perform_put(self):
        try:
            with open(self.filename, 'rb') as file:
                data = file.read(1024)
                while data:
                    self.data_socket.send(data)
                    data = file.read(1024)
        except Exception as e:
            print(f"Error while sending file:{e}")
        finally:
            self.data_socket.close()
        
        print("File sent successfully")


    def perform_get(self):
        with open(self.filename, 'wb') as file:
            data = self.data_socket.recv(1024)
            while data:
                file.write(data)
                data = self.data_socket.recv(1024)
        print("File received successfully")

    def perform_ls(self):
        file_list = self.data_socket.recv(1024).decode()
        print("File list: ")
        print(file_list)
    
    
    
def main():
    control_interface = FtpServerControlInterface()
    data_interface = FtpServerDataInterface()

    while True:
        command = input("ftp>:")
        if command == "quit":
            break
        if control_interface.connect("localhost", 8080):
            if command.startswith(FtpServerCommand.GET.value):
                filename = command.split()[1]
                data_interface.filename = filename
                data_interface.connect("localhost", 8181)
                data_interface.perform_get()
            elif command.startswith(FtpServerCommand.PUT.value):
                filename = command.split()[1]
                data_interface.filename = filename
                data_interface.connect("localhost", 8181)
                data_interface.perform_put()
            elif command == FtpServerCommand.LS.value:
                data_interface.connect("localhost", 8181)
                data_interface.perform_ls()
        else:
            print("Control interface connection failed")
            

if __name__ == "__main__":
    sys.exit(main())


        
