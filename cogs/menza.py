import datetime
import discord
import asyncio
from discord.ext import commands, tasks
import util

from config import config, messages
config = config.Config
messages = messages.Messages

from features import menza

class Menza(commands.Cog):
    send_hour = 8

    def __init__(self, bot):
        self.bot = bot
        self.menza = menza.Menza()
        self.dailyMenu.start()

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

    @tasks.loop(hours=24)
    async def dailyMenu(self):
        """Send the daily menu to #food, if the current day is not loaded -> fetch"""
        
        today = datetime.datetime.today()
        if today.isoweekday() in [6,7]:
            # Skip weekends
            return
        
        today = today.strftime("%d.%m.%Y")
        channel = self.bot.get_channel(config.food_id)
        if channel is not None:
            if not self.menza.isLoaded(today):
                await channel.send(await self.fetch())

            day = self.menza.get(today)
            await channel.send(f"```{day}```")

    @dailyMenu.before_loop
    async def before(self):
        await self.bot.wait_until_ready()

        print("Started waiting for the specified time")

        while datetime.datetime.now().hour != self.send_hour:
            await asyncio.sleep(60)
            
        print("Started menu loop")

    @commands.command()
    async def menza(self, ctx, cmd: str = "", subcmd: str = ""):
        """Menza operations"""
        msg = ""

        if cmd == "":
            msg = messages.menza_help

        elif cmd == "get":
            day = self.menza.get(subcmd)
            if day:
                msg = f"```{day}```"
            elif subcmd == "":
                msg = self.menza.listDates()
            else:
                msg = messages.menza_get_failed.format(dates=self.menza.listDates())

        elif cmd == "dump":
            msg = f"```{self.menza.get(subcmd).dump(ret=True)}```"

        elif cmd == "fetch":
            msg = await self.fetch()

        elif cmd == "timestamp":
            msg = str(self.menza.timestamp)

        elif cmd == "sethour":
            try:
                if not 0 <= int(subcmd) <= 23:
                    raise ValueError

                self.send_hour = int(subcmd)
                self.dailyMenu.restart()
                msg = messages.menza_sethour_success

            except ValueError:
                msg = messages.menza_sethour_failed

        else:
            msg = messages.menza_nocommand

        await ctx.send(msg)

def setup(bot):
    bot.add_cog(Menza(bot))
