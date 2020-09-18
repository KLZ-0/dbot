import os
import datetime
from config import config

config = config.Config


def command_list():
    with open(os.path.join(os.path.dirname(__file__), "commands.md"), "r", encoding="utf-8") as f:
        txt = f.read()
    return txt


def log(*args):
    if os.getenv("DBOT_SILENTLOG", False):
        with open(config.logfile, "a") as f:
            f.write(f"[{datetime.datetime.now()}] {''.join(args)}\n")
    else:
        print("".join(args))


def git_head_hash():
    with open(".git/refs/heads/master", "r") as f:
        return f.read()
