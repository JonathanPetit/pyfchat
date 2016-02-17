import socket
import sys

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
        self.user = {}

    def run(self):
        print("Listening on " + addressserveur[0] + ":%i" % addressserveur[1])

        self.socket.listen(0)

        while True:
            client, addressip = self.socket.accept()
            try:
                self._handle(client)
                client.shutdown(1)
                client.close()
            except OSError:
                print('Erreur traitement requête client')

    def _handle(self, client):
        response = self._recv(client)
        print(response)

    def _recv(self, client):
        response = b""
        r = client.recv(1024)
        while r:
            response += r
            r = client.recv(1024)

        return response.decode()
