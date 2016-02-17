import socket
import pickle
from colorama import Fore


class Client:
    def __init__(self, username):
        self.nickname = username
        self.adress = socket.gethostname()
        self.socket = socket.socket()

        # By default the server points to localhost
        self.server = socket.gethostname()
        self.server_port = 5000

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
            self.server_port = 5000

    def send_available_to_server(self):
        try:
            self.socket.connect((self.server, self.server_port))
            self._send("AVAILABLE " + self.username)
            response = self._recv()
            print(response)
            self.socket.close()
        except OSError:
            print(Fore.RED + "Impossible to connect: Server not found")

    def _send(self, message):
        try:
            totalsent = 0
            msg = pickle.dumps(message)

            while totalsent < len(msg):
                sent = self.socket.send(msg[totalsent:])
                totalsent += sent

        except OSError:
            print(Fore.RED + "Server error")

    def _recv(self):
        response = []
        r = self.socket.recv(1024)
        while r:
            response += r
            r = self.socket.recv(1024)

        return pickle.loads(response)

    def run(self):
        self.send_available_to_server()
