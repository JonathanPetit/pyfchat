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

        self._run = True

        # By default the server points to localhost
        self.server = socket.gethostname()
        self.server_port = 6000
        self.server_socket = socket.socket()
        self.server_socket.settimeout(0.5)

        # UDP connection
        self.udp_socket = socket.socket(type=socket.SOCK_DGRAM)
        self.udp_socket.settimeout(0.5)

        # use random port
        self.udp_port = random.randint(0, 65535)

        # Try to bind to a specific port, handle if port is already in use
        try:
            self.udp_socket.bind((util.show_ip(), self.udp_port))
        except socket.error as e:
            if e.errno == 98:
                print(Fore.YELLOW + "Port is already in use")
                sys.exit(1)

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

    def _handle_command(self, command, args):
        commands = {
            "quit": self._command_quit,
            "userlist": self._command_userlist,
            "connect": self._command_connect,
            "help": self._command_help,
        }

        if command in commands:
            commands[command](args)
        else:
            print(Fore.RED + "Invalid command, type ':help' for a list of available commands")

    #
    # Send "AVAILABLE username" to the server
    #
    def send_available_to_server(self):
        try:
            # print("Connecting to: " + self.server + ":%i" % self.server_port)
            self.server_socket = socket.socket()
            self.server_socket.connect((self.server, self.server_port))
            self.server_socket.sendall(pickle.dumps("AVAILABLE {0} {1}".format(self.username, self.udp_port)))
            self.server_socket.shutdown(1)
            response = self._recv()
            self.server_socket.close()

            return response

        except OSError as e:
            print(Fore.RED + "Impossible to connect: Server not found (" + str(e) + ")")
            print(Fore.RED + self.server + ":" + str(self.server_port))

    def _command_userlist(self, args=None):
        if not len(args) == 0:
            print(Fore.YELLOW + "Invalid arguments")
            self._command_help()
            return

        self.request_userlist()

    def request_userlist(self):
        try:
            self.server_socket = socket.socket()
            self.server_socket.connect((self.server, self.server_port))
            self.server_socket.sendall(pickle.dumps("USERLIST"))
            self.server_socket.shutdown(1)
            response = self._recv()
            self.server_socket.close()

            # Print the user list
            print(Fore.BLUE + "\nUsers connected:")
            print(Fore.BLUE + "----------------")

            for name in response:
                print(" ", name)

            print("")

            return response

        except OSError as e:
            print(Fore.RED + "\nImpossible to connect: Server not found")
            print(Fore.RED + self.server + ":" + str(self.server_port))
            print(Fore.RED + str(e))

    def _command_connect(self, args):
        if not len(args) == 1:
            print(Fore.YELLOW + "Invalid arguments")
            self._command_help()
            return

        self.connect_to_user(args[0])

    def connect_to_user(self, username):
        try:
            self.server_socket = socket.socket()
            self.server_socket.connect((self.server, self.server_port))
            self.server_socket.sendall(pickle.dumps("CONNECT " + username))
            self.server_socket.shutdown(1)
            response = self._recv()
            self.server_socket.close()

            print(response)

        except OSError as e:
            print(Fore.RED + "\nImpossible to connect: Server not found")
            print(Fore.RED + self.server + ":" + str(self.server_port))
            print(Fore.RED + str(e))

    def _command_quit(self, args=None):
        if not len(args) == 0:
            print(Fore.YELLOW + "Invalid arguments")
            self._command_help()
            return

        self._run = False

    def _command_help(self, args=None):
        print("\nAvailable commands:\n")
        print(":quit               | quits the program")
        print(":userlist           | displays a list of available users")
        print(":connect <username> | connects to user <username>")
        print(":help               | displays this help message")
        print("")

    def _recv(self):
        response = b""
        r = self.server_socket.recv(1024)
        while r:
            response += r
            r = self.server_socket.recv(1024)

        return pickle.loads(response)

    def run(self):
        r = ""
        while not r == "OK":
            response = self.send_available_to_server()

            # If server is unavailable
            if response is None:
                print("Exiting...")
                sys.exit(1)

            try:
                r, args = util.parse_command(response)
            except ValueError:
                print(Fore.RED + "Internal server error")
                print("Exiting...")
                sys.exit(1)

            if r == "ERROR" and args[0] == "E02":
                print(Fore.YELLOW + "This username \"%s\" is already taken, please choose another" % self.username)
                self.ask_username()

        while self._run:
            line = sys.stdin.readline().rstrip()

            # Skip if empty line
            if len(line) == 0:
                continue

            # If line begins with a colon it's considered a command
            if line[0] == ":" and len(line) > 2:
                command, args = util.parse_command(line[1:])
                self._handle_command(command, args)
