import os

def command_list():
    with open(os.path.join(os.path.dirname(__file__), "commands.md"), "r", encoding="utf-8") as f:
        txt = f.read()
    return txt
