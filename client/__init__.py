import socket
from colorama import Fore


class Client:
    def __init__(self, username):
        self.username = username
        self.adress = socket.gethostname()
        self.socket = socket.socket()

        # By default the server points to localhost
        self.server = socket.gethostname()
        self.server_port = 6000

    def set_server(self, server):
        if len(server) < 1:
            self.server = socket.gethostname()
        else:
            self.server = server

    def set_port(self, port):
        try:
            self.server_port = int(port)
        except ValueError:
            print(Fore.RED + "Not a valid port number, 5000 will be used instead")
            self.server_port = 6000

    def send_available_to_server(self):
        try:
            print("Connecting to: " + self.server + ":%i" % self.server_port)
            self.socket.connect((self.server, self.server_port))
            self.socket.sendall("AVAILABLE {0}".format(self.username).encode())
            self.socket.shutdown(1)
            response = self._recv()
            print(response)
            self.socket.close()
        except OSError:
            print(Fore.RED + "Impossible to connect: Server not found")

    def _recv(self):
        response = b""
        r = self.socket.recv(1024)
        while r:
            response += r
            r = self.socket.recv(1024)

        return response.decode()

    def run(self):
        self.send_available_to_server()
