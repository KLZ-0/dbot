import os

class Config:
    key = ""
    command_prefix = "!"

    logfile = "dbot.log"

    extensions = ["base", "cmds", "timetable", "parser", "menza"]

    tt_db = os.path.join(os.path.dirname(__file__), "timetable.db")
    bot_room_id = 624919976561737728
    bot_dev_id = 624895168839024647
    food_id = 633735827477889025

    admin_id = 0
    guild_id = 0
