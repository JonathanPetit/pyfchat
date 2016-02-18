import shlex


def parse_command(string):
    if len(string) < 1:
        raise ValueError("Empty string")
    parts = shlex.split(string)
    return (parts[0], parts[1:])
