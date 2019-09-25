import discord
from discord.ext import commands
import util
import traceback

from config import config, messages
config = config.Config
messages = messages.Messages

class Parser(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #                          #
    #      Message parser      #
    #                          #

    @commands.Cog.listener()
    async def on_message(self, message):
        channel = message.channel

        if not message.author.bot:
            # React to user messages only
            if messages.uhoh in message.content.lower():
                await channel.send(messages.uhoh)

            elif "PR" in message.content:
                await channel.send(messages.pr_meme)

def setup(bot):
    bot.add_cog(Parser(bot))
