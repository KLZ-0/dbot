from discord.ext import commands
from collections import deque

from config import config, messages
config = config.Config
messages = messages.Messages


class Parser(commands.Cog):
    message_cache = deque(maxlen=config.message_chain_size)  # used for emoji chain

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

            elif message.content.startswith(messages.pr_match):
                await message.channel.send(messages.pr_meme)

            else:
                self.message_cache.append(message.content)
                if len(set(self.message_cache)) <= 1 and len(self.message_cache) == config.message_chain_size:
                    await message.channel.send(self.message_cache[0])

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if str(payload.emoji) == "📌":
            guild = self.bot.get_guild(config.guild_id)
            channel = guild.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            if message.pinned:
                return
            await message.pin()


def setup(bot):
    bot.add_cog(Parser(bot))
