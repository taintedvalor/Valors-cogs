import discord
from redbot.core import commands
import random

class Womp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='womp')
    async def womp_group(self, ctx):
        pass

    @womp_group.command(name='toggle')
    async def toggle_womp(self, ctx):
        # Toggle the womp functionality for the guild
        pass

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if "womp" in message.content.lower():
            random_amount = random.randint(1, 10)
            punctuation = random.choice(['.', '!', '?'])
            capitalization = random.choice([str.capitalize, str.upper])
            randomized_womp = ''.join([capitalization(char) if i % 2 == 0 else char for i, char in enumerate("womp" * random_amount)])

            response = f"{randomized_womp}{punctuation}"
            await message.channel.send(response)

def setup(bot):
    bot.add_cog(Womp(bot))
