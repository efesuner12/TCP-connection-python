import socket
import threading
import time

client_list = []

class Command_Handler:

    def __init__(self, client_socket):
        self.client_socket = client_socket

    def handle(self, command):
        server_sender = Server_Sender(self.client_socket)

        if (command == "hello"):
            server_sender.send("server: Hello\n")
        else:
            server_sender.send("server: Not a valid command!\n")

class Server_Sender:

    def __init__(self, client_socket):
        self.client_socket = client_socket

    def send(self, data):
        size = str(len(data.encode("utf-8")))
        self.client_socket.send(bytes(size, "utf-8"))
        time.sleep(0.5)
        self.client_socket.send(bytes(data, "utf-8"))

class Server_Receiver:

    def __init__(self, client_socket):
        self.client_socket = client_socket

    def receive(self):
        size = int(self.client_socket.recv(10))
        return self.client_socket.recv(size)

class Client_Handler:
    
    def __init__(self, client_socket, client_info):
        self.client_socket = client_socket
        self.client_info = client_info

    def launch(self):
        server_receiver = Server_Receiver(self.client_socket)
        server_sender = Server_Sender(self.client_socket)
        command_handler = Command_Handler(self.client_socket)

        client_list.append(str(self.client_info))

        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        server_sender.send(f"Welcome to {ip_address}")

        while True:
            received_data = server_receiver.receive()
            command_handler.handle(received_data.decode("utf-8"))

class Client_Connection:

    def __init__(self) -> None:
        self.PORT = 1234

    def connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("127.0.0.1", self.PORT))
        s.listen(5)

        while True:
            client_socket, address = s.accept()
            address = str(":".join([str(item) for item in address]))
            client_handler = Client_Handler(client_socket, address)
            thread = threading.Thread(target = client_handler.launch).start()


if __name__ == "__main__":
    client_conn = Client_Connection()
    client_conn.connect()
