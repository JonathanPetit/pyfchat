import socket
import pickle
import sys
import random
from colorama import Fore, Style

import util


class Client:
    def __init__(self):
        self.username = "guest" + str(random.randint(100, 99999))
        self.adress = socket.gethostname()
        self.socket = socket.socket()

        # By default the server points to localhost
        self.server = socket.gethostname()
        self.server_port = 6000

    def ask_username(self):
        self.set_username(
            input("Enter your username " + Style.DIM + "(current = " + self.username + "): " + Style.RESET_ALL)
        )

    def ask_server(self):
        self.set_server(
            input("Enter server " + Style.DIM + "(current = " + self.server + "): " + Style.RESET_ALL)
        )

    def ask_port(self):
        self.set_port(
            input("Enter port " + Style.DIM + "(current = " + str(self.server_port) + "): " + Style.RESET_ALL)
        )

    def set_username(self, username):
        if len(username) < 1:
            return
        else:
            self.username = username

    def set_server(self, server):
        if len(server) < 1:
            return
        else:
            self.server = server

    def set_port(self, port):
        # If nothing has been specified use current
        if len(port) < 1:
            return
        try:
            self.server_port = int(port)
        except ValueError:
            print(Fore.RED + "Not a valid port number, 6000 will be used instead")
            self.server_port = 6000

    #
    # Send "AVAILABLE username" to the server
    #
    def send_available_to_server(self):
        try:
            print("Connecting to: " + self.server + ":%i" % self.server_port)
            self.socket = socket.socket()
            self.socket.connect((self.server, self.server_port))
            self.socket.sendall(pickle.dumps("AVAILABLE {0}".format(self.username)))
            self.socket.shutdown(1)
            response = self._recv()
            self.socket.close()

            return response

        except OSError as e:
            print(Fore.RED + "Impossible to connect: Server not found")
            print(Fore.RED + self.server + ":" + str(self.server_port))
            print(Fore.RED + str(e))

    def request_userlist(self):
        try:
            print("Connecting to: " + self.server + ":%i" % self.server_port)
            self.socket = socket.socket()
            self.socket.connect((self.server, self.server_port))
            self.socket.sendall(pickle.dumps("USERLIST"))
            self.socket.shutdown(1)
            response = self._recv()
            self.socket.close()

            return response

        except OSError as e:
            print(Fore.RED + "Impossible to connect: Server not found")
            print(Fore.RED + self.server + ":" + str(self.server_port))
            print(Fore.RED + str(e))


    def _recv(self):
        response = b""
        r = self.socket.recv(1024)
        while r:
            response += r
            r = self.socket.recv(1024)

        return pickle.loads(response)

    def run(self):
        r = ""
        while not r == "OK":
            response = self.send_available_to_server()
            print(response)
            try:
                r, args = util.parse_command(response)
            except ValueError:
                print(Fore.RED + "Internal server error")
                print("Aborting...")
                sys.exit(1)

            if r == "ERROR" and args[0] == "E01":
                print(Fore.YELLOW + "This username (%s) is already taken, please choose another")
                self.ask_username()
        print(self.request_userlist())
