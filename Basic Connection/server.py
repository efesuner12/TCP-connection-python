from http import client
import socket
import threading

clientList = []

class CommandHandler:

    def __init__(self, clientSocket):
        self.clientSocket = clientSocket

    def handle(self, command):
        serverSender = ServerSender(self.clientSocket)

        ###
        ### EXAMPLE COMMAND AND HANDLE
        ###
        if(command == "hello"):
            serverSender.send("server: hello\n")

class ServerSender:

    def __init__(self, clientSocket):
        self.clientSocket = clientSocket

    def send(self, data):
        size = str(len(data.encode("utf-8")))
        self.clientSocket.send(bytes(size, "utf-8"))
        self.clientSocket.send(bytes(data, "utf-8"))

class ServerReceiver:

    def __init__(self, clientSocket):
        self.clientSocket = clientSocket

    def receive(self):
        size = int(self.clientSocket.recv(10))
        return self.clientSocket.recv(size)

class ClientHandler:
    
    def __init__(self, clientSocket, clientInfo):
        self.clientSocket = clientSocket
        self.clientInfo = clientInfo

    def launch(self):
        serverReceiver = ServerReceiver(clientSocket = self.clientSocket)
        serverSender = ServerSender(clientSocket = self.clientSocket)
        commandHandler = CommandHandler(clientSocket = self.clientSocket)

        clientList.append(str(self.clientInfo))

        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        serverSender.send(f"Welcome to {ip_address}")

        while True:
            receivedData = serverReceiver.receive()
            commandHandler.handle(receivedData.decode("utf-8"))

class ClientConnection:

    def __init__(self) -> None:
        self.PORT = 1234

    def connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("127.0.0.1", self.PORT))
        s.listen(5)

        while True:
            clientSocket, address = s.accept()
            address = str(":".join([str(item) for item in address]))
            clientHandler = ClientHandler(clientSocket, address)
            thread = threading.Thread(target = clientHandler.launch).start()


class Main:

    if __name__ == "__main__":
        clientConn = ClientConnection()
        clientConn.connect()
