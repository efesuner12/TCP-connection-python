import socket

class CommandHandler:

    def __init__(self, serverSocket):
        self.serverSocket = serverSocket

    def handle(self, command):
        clientSender = ClientSender(serverSocket = self.serverSocket)
        clientReceiver = ClientReceiver(serverSocket = self.serverSocket)

        clientSender.send(command)
        feedback = clientReceiver.receive().decode("utf-8")
        print(feedback)

class ClientSender:

    def __init__(self, serverSocket):
        self.serverSocket = serverSocket

    def send(self, data):
        size = str(len(data.encode("utf-8")))
        self.serverSocket.send(bytes(size, "utf-8"))
        self.serverSocket.send(bytes(data, "utf-8"))

class ClientReceiver:

    def __init__(self, serverSocket):
        self.serverSocket = serverSocket

    def receive(self):
        size = int(self.serverSocket.recv(10))
        return self.serverSocket.recv(size)

class ServerConnection:
    
    def __init__(self, ip):
        self.PORT = 1234
        self.ip = ip

    def connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip, self.PORT))

        return s


class Main:

    if __name__ == "__main__":
        ipAddr = input("Please enter the ip-address:\n--> ")

        serverConnection = ServerConnection(ipAddr)
        serverSocket = serverConnection.connect()

        clientReceiver = ClientReceiver(serverSocket = serverSocket)

        message = clientReceiver.receive().decode("utf-8")
        print(f"\n{message}\n")

        while True:
                command = input("--> ")

                while command != "":
                    comandHandler = CommandHandler(serverSocket = serverSocket)
                    comandHandler.handle(command = command)
                    command = input("--> ")
                    
                print()
