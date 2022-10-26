import socket
import time

class Validator:

    def valid_IP_address(self, ip_address):

        if ip_address.upper() == "QUIT":
            print("\nBYE!")
            exit(0)

        def is_IPv4(s):
            try: 
                return str(int(s)) == s and 0 <= int(s) <= 255
            except: 
                return False
        
        if ip_address.count(".") == 3 and all(is_IPv4(i) for i in ip_address.split(".")):
            return True

        return False

class Command_Handler:

    def __init__(self, server_socket):
        self.server_socket = server_socket

    def handle(self, command):
        if (command.upper() == "QUIT"):
            print("\nBYE!")
            exit(0)

        client_sender = Client_Sender(self.server_socket)
        client_receiver = Client_Receiver(self.server_socket)

        if (client_sender.send(command)):
            feedback = client_receiver.receive().decode("utf-8")
            print(feedback)

class Client_Sender:

    def __init__(self, server_socket):
        self.server_socket = server_socket

    def send(self, data):
        try:
            size = str(len(data.encode("utf-8")))
            self.server_socket.send(bytes(size, "utf-8"))
        except:
            print(f"There has been an error while sending the size!\n")
            return False
        
        time.sleep(0.5)
        
        try:
            self.server_socket.send(bytes(data, "utf-8"))
        except:
            print(f"There has been an error while sending the data!\n")
            return False

        return True

class Client_Receiver:

    def __init__(self, server_socket):
        self.server_socket = server_socket

    def receive(self):
        try:
            size = int(self.server_socket.recv(5))
            return self.server_socket.recv(size)
        except Exception as e:
            return bytes(f"There has been an error while receiving the data!\nError message: {e}", "utf-8")

class Server_Connection:
    
    def __init__(self, ip):
        self.PORT = 1234
        self.ip = ip

    def connect(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            s.connect((self.ip, self.PORT))
            s.settimeout(None)
        except socket.error:
            return f"Could not connect to {self.ip}\nPlease make sure host is up and try again...\n"

        return s


if __name__ == "__main__":
    ip_addr = input("Please enter the host's IP address: (QUIT to exit)\n--> ")

    validator = Validator()
    valid_ip = validator.valid_IP_address(ip_addr)

    while not(valid_ip):
        print(f"'{ip_addr}' is not a valid IP Address!\nPlease enter a valid IP and try again...\n")
        ip_addr = input("Please enter the host's IP address: (QUIT to exit)\n--> ")
        valid_ip = validator.valid_IP_address(ip_addr)

    server_connection = Server_Connection(ip_addr)
    server_socket = server_connection.connect()

    while not(type(server_socket) == socket.socket):
        print(server_socket)

        ip_addr = input("Please enter the host's IP address: (QUIT to exit)\n--> ")
        valid_ip = validator.valid_IP_address(ip_addr)

        while not(valid_ip):
            print(f"'{ip_addr}' is not a valid IP Address!\nPlease enter a valid IP and try again...\n")
            ip_addr = input("Please enter the host's IP address: (QUIT to exit)\n--> ")
            valid_ip = validator.valid_IP_address(ip_addr)
        
        server_connection = Server_Connection(ip_addr)
        server_socket = server_connection.connect()

    client_receiver = Client_Receiver(server_socket)

    message = client_receiver.receive().decode("utf-8")
    print(f"{message}\n")

    while True:
        command = input("Please enter a command: (QUIT to exit)\n--> ")

        while command.upper() != "":
            comand_handler = Command_Handler(server_socket)
            comand_handler.handle(command)
            command = input("Please enter a command: (QUIT to exit)\n--> ")
            
        print()
