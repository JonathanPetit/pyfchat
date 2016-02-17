import socket
import sys

from colorama import Fore

addressserveur = (socket.gethostname(), 6000)


class Server:

    def __init__(self):
        self.socket = socket.socket()

        # Try to bind to a specific port, handle if port is already in use
        try:
            self.socket.bind(addressserveur)
        except socket.error as e:
            if e.errno == 98:
                print("Port is already in use")
                sys.exit(1)

        self.address = socket.gethostname()
        self.users = {}

    def run(self):
        print("Listening on " + addressserveur[0] + ":%i" % addressserveur[1])

        self.socket.listen(0)

        while True:
            client, ipaddress = self.socket.accept()
            try:
                self._handle(client, ipaddress)
                client.shutdown(1)
                client.close()
            except OSError:
                print(Fore.RED + 'Erreur traitement requête client')

    def _handle(self, client, ip):
        request = self._recv(client)
        command, args = parse_request(request)

        if command == "AVAILABLE":
            self._handle_command_available(ip, args)
        else:
            print(Fore.YELLOW + "Invalid request")

    def _handle_command_available(self, ip, args):
        if not len(args) == 1:
            print(Fore.YELLOW + "Invalid request")
            return

        username = args[0]

        # If the username is in the list check if the ip adress is the same
        if username in self.users:
            if not ip == self.users.get(username):
                print(Fore.RED + "Username is already in use")
        else:
            self.users[username] = ip
            print(Fore.GREEN + "User added:", username, ip)

    def _recv(self, client):
        response = b""
        r = client.recv(1024)
        while r:
            response += r
            r = client.recv(1024)

        return response.decode()


def parse_request(request):
    r = request.strip().split()

    if len(r) < 2:
        print(Fore.YELLOW + "Invalid request")
        return

    command = r[0]
    args = r[1:]

    return (command, args)
