"""pyfchat simple chat with file transfer ability."""
import sys
from server import Server
from client import Client


def print_help():
    """print help."""
    print("""Welcome to pyfchat

CLIENT MODE:
    Launch the client mode by calling the utility without any arguments

    `python pyfchat.py`

SERVER MODE:
    Launch the server mode by calling the utility with "server" as first argument

    `python pyfchat.py server`

    """)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        Client().run()
    else:
        if sys.argv[1] == 'server':
            Server().run()
        else:
            print_help()
