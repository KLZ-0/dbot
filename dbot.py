import discord
from discord.ext import commands

from config import config, messages
config = config.Config
messages = messages.Messages

bot = commands.Bot(command_prefix=config.command_prefix)

@bot.event
async def on_ready():
    """If DBOT is ready"""
    print("Started fetching")
    await bot.cogs["Menza"].fetch(debug=True)
    print("Ready")

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")

@bot.command()
async def unload(ctx, extension):
    bot.load_extension(f"cogs.{extension}")

for extension in config.extensions:
    bot.load_extension(f'cogs.{extension}')
    print(f'{extension} loaded')

bot.run(config.key)
