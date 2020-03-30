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
        if not message.author.bot:
            # React to user messages only
            if messages.uhoh in message.content.lower():
                await message.channel.send(messages.uhoh)

            elif message.content == messages.pr_match:
                await message.channel.send(messages.pr_meme)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if str(payload.emoji) == "📌":
            guild = self.bot.get_guild(config.guild_id)
            channel = guild.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            if (message.pinned): return
            await message.pin()

def setup(bot):
    bot.add_cog(Parser(bot))
