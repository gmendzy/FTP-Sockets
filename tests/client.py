import socket
def main():

    # Client configuration
    server_host = "localhost"  # Specify the server's IP or hostname
    control_port = 8080  # Control channel for transferring all commands to server from client , initial channel for which the client will connect to the server. 
    
    client_control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_control_socket.connect((server_host, control_port))

    while True:
        command = input("ftp> ").strip()
        client_control_socket.send(command.encode())

        if command == "quit":
            break
        
        data_port = int(client_control_socket.recv(1024).decode())
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_socket.connect((server_host, data_port))

        if command.startswith("get"):
            filename = command.split(" ")[1]
            handle_get(data_socket, filename)
        elif command.startswith("put"):
            filename = command.split(" ")[1]
            handle_put(data_socket, filename)
        elif command == "ls":
            handle_ls(data_socket)
        
        data_socket.close()
    client_control_socket.close()



def handle_put(data_socket, filename):
    with open(filename, 'rb') as file:
        data = file.read(1024)
        while data:
            data_socket.send(data)
            data = file.read(1024)
    print("File sent successfully")


def handle_get(data_socket, filename):
    with open(filename, 'wb') as file:
        data = data_socket.recv(1024)
        while data:
            file.write(data)
            data = data_socket.recv(1024)
    print("File received successfully")

def handle_ls(data_socket):
    file_list = data_socket.recv(1024).decode()
    print("File list: ")
    print(file_list)
    


if __name__ == "__main__":
    main()
