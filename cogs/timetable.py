import sqlite3
import datetime
import discord
import asyncio
import os
from discord.ext import commands

from config import config, messages, semester
config = config.Config
messages = messages.Messages
semester = semester.Semester

class Timetable(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def getTimetable(self, weekday):
        weeknumber = datetime.datetime.now().isocalendar()[1]
        conn = sqlite3.connect(getattr(config, "tt_db", "timetable.db"))
        c = conn.cursor()

        daystr = messages.tt_header.format(day=messages.tt_days_cz[weekday])
        for line in c.execute('SELECT * FROM timetable WHERE day=?', str(weekday)):
            # NOTE: Weekdays start from 0 = monday
            # TODO: Rewrite these awful lines
            if str(line[0]) == "1" and line[1] == "IUS" and weeknumber not in semester.rare_subjects["IUS"]:
                # filter IUS allow only n times per semester
                continue

            if str(line[0]) == "3" and line[1] == "IEL" and weeknumber % 2 == 0:
                # filter IEL, allow only odd weeks
                continue

            daystr += messages.tt_line.format(
                name=line[1], start=line[2], end=line[3], rooms=line[4], detail=line[5])

        if weekday in semester.prezuvky:
            daystr += messages.tt_prezuvky_needed

        conn.close()
        return daystr

    @commands.command()
    async def rozvrh(self, ctx, weekday: int = datetime.datetime.today().weekday()+1):
        if not os.path.isfile(getattr(config, "tt_db", "timetable.db")):
            await ctx.send(messages.tt_db_error)
            return

        await ctx.send(self.getTimetable(weekday-1))

   


def setup(bot):
    bot.add_cog(Timetable(bot))
