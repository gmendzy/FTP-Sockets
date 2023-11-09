import socket

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

            if command.startswith("put"):
                self.data_port = int(client_socket.recv(1024).decode())
                data_socket = self.data_connection()
                filename = command.split()[1]
                self.put(data_socket, filename)

        client_socket.close()

    def data_connection(self):
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_socket.connect((self.addr, self.data_port))
        return data_socket

    def put(self, data_socket, filename):
        with open(filename, 'rb') as file:
            data = file.read(1024)
            while data:
                data_socket.send(data)
                data = file.read(1024)
            data_socket.close()
        print("File sent successfully.")

if __name__ == "__main__":
    ftp_client = FtpClient()
    ftp_client.start()
