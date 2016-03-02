import socket
import sys
import pickle
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

    def run(self):
        print(Fore.BLUE + "Listening on " + util.show_ip() + ":%i" % 6000)

        self.socket.listen(0)

        while True:
            client, ipaddress = self.socket.accept()
            try:
                self._handle(client, ipaddress[0])
                client.shutdown(1)
                client.close()
            except OSError:
                print(Fore.RED + 'Erreur traitement requête client')

    def _handle(self, client, ip):
        request = self._recv(client)
        command, args = util.parse_command(request)

        commands = {
            "AVAILABLE": self._handle_command_available,
            "CONNECT": self._handle_connect_request,
            "USERLIST": self._handle_userlist_request,
            "REMOVE": self._remove
        }

        if command in commands:
            commands[command](client, args)
        else:
            self._invalid_request(client)

    def _invalid_request(self, client):
        print(Fore.YELLOW + "Invalid request")
        client.sendall(pickle.dumps("ERROR E01 'Invalid request'"))

    def _remove(self, client, args):
        if not len(args) == 1:
            self._invalid_request(client)
            return

        ip = args[0]

        for username in self.users:
            if ip == self.users[username][0]:
                del self.users[username]
                print(Fore.YELLOW + "User removed: " + Fore.RESET + username)
                break

    def _handle_command_available(self, client, args):
        if not len(args) == 3:
            self._invalid_request(client)
            return

        ip = args[0]
        username = args[1]
        port = args[2]

        # If the username is in the list check if the ip adress is the same
        if username in self.users:
            if not (ip, port) == self.users[username]:
                print(Fore.RED + "Username is already in use")
                client.sendall(pickle.dumps("ERROR E02 'Username already in use'"))
            else:
                print("User \"" + username + "\" pinged")
                client.sendall(pickle.dumps("OK"))

        else:
            self.users[username] = (ip, port)
            print(Fore.GREEN + "User added:", username, ip, port, Fore.RESET)
            client.sendall(pickle.dumps("OK"))

    def _handle_connect_request(self, client, args):
        if not len(args) == 1:
            self._invalid_request(client)
            return

        username = args[0]

        user = self.users.get(username)

        # If the username is in the list check if the ip adress is the same
        if user is None:
            print(Fore.RED + "User does not exist")
            client.sendall(pickle.dumps("ERROR E03 'User does not exist'"))
            return

        client.sendall(pickle.dumps(user))

    def _handle_userlist_request(self, client, args):
        listusers = []
        for users in self.users:
            listusers.append(users)

        client.sendall(pickle.dumps(listusers))

    def _recv(self, client):
        response = b""
        r = client.recv(1024)
        while r:
            response += r
            r = client.recv(1024)

        return pickle.loads(response)

    #
    # Helper function for commands that are not yet implemented
    #
    def _command_unimplemented(self, client, ip, args):
        print(Fore.YELLOW + "Ow, It seems I am not implemented yet..")

    def _userlist(self, client, ip, args):
        listusers =[]
        for users in self.users:
            listusers.append(users)
        sendusers = ', '.join(listusers)
        client.sendall(pickle.dumps(sendusers))
        client.sendall(pickle.dumps("OK"))
