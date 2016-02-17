#Available ==> message ok et username
#liste vide ==> remplir adresse ip et username
#si il est dans la liste erreur
#sinon message ok

import pickle
import socket
import struct
import sys

addressserveur = (socket.gethostname(), 6000)

class Server:

    def __init__(self):
        self.socket = socket.socket()
        self.socket.bind(addressserveur)
        self.address = socket.gethostname()
        self.user = {}

    def run(self):
        print("Listening on " + addressserveur[0] + ":%i" % addressserveur[1])
        #Ecoute sur un port
        self.socket.listen(0)
        while True:
            #Renvoi socket sous forme de tuple client, ip
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
