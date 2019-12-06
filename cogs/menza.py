import datetime
import discord
import asyncio
from discord.ext import commands
import util

from config import config, messages
config = config.Config
messages = messages.Messages

from features import menza

class Menza(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.menza = menza.Menza()

    async def fetch(self, debug=False):
        msg = ""
        if await self.menza.fetch():
            msg = messages.menza_fetch_success
        else:
            msg = messages.menza_fetch_failed
        
        if debug:
            print(msg)
        else:
            return msg

    @commands.command()
    async def menza(self, ctx, subcmd: str = "", date: str = ""):
        """Menza operations"""
        msg = ""

        if subcmd == "":
            msg = messages.menza_help

        elif subcmd == "get":
            day = self.menza.get(date)
            if day:
                msg = f"```{day}```"
            elif date == "":
                msg = self.menza.listDates()
            else:
                msg = messages.menza_get_failed.format(dates=self.menza.listDates())

        elif subcmd == "dump":
            msg = f"```{self.menza.get(date).dump(ret=True)}```"

        elif subcmd == "fetch":
            msg = await self.fetch()

        elif subcmd == "timestamp":
            msg = str(self.menza.timestamp)

        else:
            msg = messages.menza_nocommand

        await ctx.send(msg)

def setup(bot):
    bot.add_cog(Menza(bot))
