import os
import datetime
from config import config

config = config.Config

def command_list():
    with open(os.path.join(os.path.dirname(__file__), "commands.md"), "r", encoding="utf-8") as f:
        txt = f.read()
    return txt

def log(message):
    with open(config.logfile, "a") as f:
        f.write(f"[{datetime.datetime.now()}] {str(message)}\n")
