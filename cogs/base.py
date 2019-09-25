import discord
from discord.ext import commands
import util
import traceback

from config import config, messages
config = config.Config
messages = messages.Messages

class Base(commands.Cog):

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
            if message.content.lower().startswith(messages.uhoh):
                await channel.send(messages.uhoh)

            elif "PR" in message.content:
                await channel.send(messages.pr_meme)

            elif messages.gn in message.content:
                await channel.send(messages.gn)

            elif messages.gm in message.content:
                await channel.send(messages.gm)

    #                                    #
    #      Invalid command handler       #
    #                                    #

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandNotFound):
            await ctx.send(messages.err_unknown_command.format(commandlist=util.command_list()))

        else:
            output = f"Ignoring exception in command {ctx.command}:\n"
            output += "".join(traceback.format_exception(type(error),
                                                         error,
                                                         error.__traceback__))
            channel = self.bot.get_channel(config.bot_dev_id)
            output = list(output[0 + i: 1900 + i] for i in range(0, len(output), 1900))
            if channel is not None:
                for message in output:
                    await channel.send(f"```\n{message}\n```")

def setup(bot):
    bot.add_cog(Base(bot))
