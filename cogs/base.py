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

    #                                    #
    #      Invalid command handler       #
    #                                    #

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandNotFound):
            await ctx.send(messages.err_unknown_command.format(commandlist=util.command_list()))

        elif isinstance(error, commands.errors.BadArgument):
            await ctx.send(messages.conversion_error)

        elif isinstance(error, commands.errors.InvalidEndOfQuotedStringError):
            await ctx.send(messages.command_arg_error)
        
        elif isinstance(error, commands.errors.UnexpectedQuoteError):
            await ctx.send(messages.command_arg_error)

        elif isinstance(error, commands.errors.ExpectedClosingQuoteError):
            await ctx.send(messages.command_arg_error)

        else:
            output = f"Ignoring exception in command {ctx.command}:\n"
            output += "".join(traceback.format_exception(type(error),
                                                         error,
                                                         error.__traceback__))
            channel = self.bot.get_channel(config.bot_dev_id)
            output = list(output[0 + i: 1900 + i]
                          for i in range(0, len(output), 1900))
            if channel is not None:
                for message in output:
                    await channel.send(f"```\n{message}\n```")

    @commands.command()
    async def purge(self, ctx, n = "1", silent = ""):
        """Remove last n messages"""
        try:
            n = int(n) + 1
        except ValueError:
            return

        if n < 1 or n > 20:
            await ctx.send(messages.purge_value_error)
            return

        ids = []
        async for message in ctx.channel.history(limit=n):
            if message.author in [ctx.message.author, self.bot.user]:
                ids.append(message.id)
                await message.delete()
            
        if not silent:
            await ctx.send(messages.purge_message.format(n=len(ids)-1))

        util.log(f"<PURGE> {ctx.message.author.display_name} ({ctx.message.author.id}) removed: {str(ids)}")

def setup(bot):
    bot.add_cog(Base(bot))
