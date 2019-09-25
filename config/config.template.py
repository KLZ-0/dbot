import os

class Config:
    key = ""
    command_prefix = "!"

    extensions = ["base", "cmds", "timetable", "parser"]

    tt_db = os.path.join(os.path.dirname(__file__), "timetable.db")
    bot_room_id = 624919976561737728
    bot_dev_id = 624895168839024647
