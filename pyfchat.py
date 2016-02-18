# -*-coding:Latin-1 -*
import sys

# Colors in the terminal ! :D
try:
    import colorama
except ImportError:
    print("""Please, install colorama!

pip install colorama
    """)
    sys.exit(1)

from server import Server
from client import Client


def print_help():
    print("""Welcome to pyfchat

CLIENT MODE:
    Launch the client mode by calling the utility without any arguments

    `python pyfchat.py`

SERVER MODE:
    Launch the server mode by calling the utility with "server" as first argument

    `python pyfchat.py server`

    """)

if __name__ == '__main__':
    # Initialise colorama
    colorama.init(autoreset=True)

    if len(sys.argv) < 2:

        port = 6000

        client = Client()
        client.ask_username()
        client.ask_server()
        client.ask_port()

        client.run()

    else:
        if sys.argv[1] == 'server':
            Server().run()
        else:
            print_help()
