import shlex
import socket


def parse_command(string):
    if len(string) < 1:
        raise ValueError("Empty string")
    parts = shlex.split(string)
    return (parts[0], parts[1:])


def show_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 0))  # connecting to a UDP address doesn't send packets
    except OSError:
        print("Not connected to internet")
        return socket.gethostbyname(socket.gethostname())
    return s.getsockname()[0]
