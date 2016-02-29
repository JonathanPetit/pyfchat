import socket
import sys

from colorama import Fore

import util


class Server:

    def __init__(self):
        self.socket = socket.socket()

        # Try to bind to a specific port, handle if port is already in use
        try:
            self.socket.bind(('', 6000))
        except socket.error as e:
            if e.errno == 98:
                print(Fore.YELLOW + "Port is already in use")
                sys.exit(1)

        self.address = socket.gethostname()
        self.users = {}

    #
    #
    def run(self):
        print("Listening on " + self._show_ip() + ":%i" % 6000)
        print(self._show_ip())

        self.socket.listen(0)

        while True:
            client, ipaddress = self.socket.accept()
            try:
                self._handle(client, ipaddress[0])
                client.shutdown(1)
                client.close()
            except OSError:
                print(Fore.RED + 'Erreur traitement requête client')

    #
    #
    def _handle(self, client, ip):
        request = self._recv(client)
        command, args = util.parse_command(request)

        commands = {
            "AVAILABLE": self._handle_command_available,
            "CONNECT": self._command_unimplemented,
        }

        if command in commands:
            commands[command](client, ip, args)
        else:
            self._invalid_request(client)

    #
    #
    def _invalid_request(self, client):
        print(Fore.YELLOW + "Invalid request")
        client.sendall("ERROR E01 'Invalid request'".encode())

    #
    #
    def _handle_command_available(self, client, ip, args):
        if not len(args) == 1:
            self._invalid_request(client)
            return

        username = args[0]

        # If the username is in the list check if the ip adress is the same
        if username in self.users:
            if not ip == self.users.get(username):
                print(Fore.RED + "Username is already in use")
                client.sendall("ERROR E02 'Username already in use'".encode())
            else:
                print("User \"" + username + "\" pinged")
                client.sendall("OK".encode())

        else:
            self.users[username] = ip
            print(Fore.GREEN + "User added:", username, ip, Fore.RESET)
            client.sendall("OK".encode())

    def _recv(self, client):
        response = b""
        r = client.recv(1024)
        while r:
            response += r
            r = client.recv(1024)

        return response.decode()

    #
    # Helper function for commands that are not yet implemented
    #
    def _command_unimplemented(self, client, ip, args):
        print(Fore.YELLOW + "Ow, It seems I am not implemented yet..")

    # Needs an internet connecion to work...
    def _show_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 0))  # connecting to a UDP address doesn't send packets
        except OSError:
            print("Not connected to internet")
            return socket.gethostbyname(socket.gethostname())
        return s.getsockname()[0]
