import discord
from discord.ext import commands
import util

from config import config, messages
config = config.Config
messages = messages.Messages

bot = commands.Bot(command_prefix=config.command_prefix)

util.log("====== DBOT STARTED ======")

@bot.event
async def on_ready():
    """If DBOT is ready"""
    util.log("Started fetching")
    await bot.cogs["Menza"].fetch(debug=True)
    util.log("Ready")

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")

@bot.command()
async def unload(ctx, extension):
    bot.load_extension(f"cogs.{extension}")

for extension in config.extensions:
    bot.load_extension(f'cogs.{extension}')
    util.log(f'{extension} loaded')

bot.run(config.key)
