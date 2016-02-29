import socket
import sys
import random
from colorama import Fore, Style
import pickle

import util


class Client:
    def __init__(self):
        self.username = "guest" + str(random.randint(100, 99999))
        self.adress = socket.gethostname()

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
        self.udp_socket.bind((util.show_ip(), self.udp_port))


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
            self.server_socket = socket.socket()
            self.server_socket.connect((self.server, self.server_port))
            self.server_socket.sendall(pickle.dumps("AVAILABLE {0} {1}".format(self.username, self.udp_port)))
            self.server_socket.shutdown(1)
            response = self._recv()
            self.server_socket.close()

            return response

        except OSError as e:
            print(Fore.RED + "Impossible to connect: Server not found")
            print(Fore.RED + self.server + ":" + str(self.server_port))
            print(Fore.RED + str(e))

    def _handle(self):
        commands = {
            '/exit': self._exit,
            '/quit': self._quit,
            '/join': self._join,
            '/send': self._send
        }

    def _exit(self):
        self.running= False
        self.udp_socket.close()



    def _quit(self):
        pass

    def _join(self):
        name = input('Which users would you connect?:')
        users = name.split(' ')
        try:
            self.__address = (socket.gethostbyaddr(tokens[0])[0], int(tokens[1]))
            print('Connecté à {}:{}'.format(*self.__address))
        except OSError:
            print("Erreur lors de l'envoi du message.")

    def request_userlist(self):
        try:
            self.server_socket = socket.socket()
            self.server_socket.connect((self.server, self.server_port))
            self.server_socket.sendall(pickle.dumps("USERLIST"))
            self.server_socket.shutdown(1)
            response = self._recv()
            print(response)
            self.server_socket.close()
            return print(Fore.BLUE + "Userlist connect: " + response)

        except OSError as e:
            print(Fore.RED + "Impossible to connect: Server not found")
            print(Fore.RED + self.server + ":" + str(self.server_port))
            print(Fore.RED + str(e))

    def _recv(self):
        response = b""
        r = self.server_socket.recv(1024)
        while r:
            response += r
            r = self.server_socket.recv(1024)

        return pickle.loads(response)


    def run(self):
        self.__running = True
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

            if r == "ERROR" and args[0] == "E02":
                print(Fore.YELLOW + "This username \"%s\" is already taken, please choose another" % self.username)
                self.ask_username()
        while self.running:
            try:
                message, adress = self.udp_socket.recvfrom(1024)
            except udp_socket.timeout:
                pass
            except OSError:
                return

        print(self.request_userlist())
