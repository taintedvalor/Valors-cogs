import discord
from redbot.core import commands, Config
import random

class Womp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)  # Replace with your own unique identifier
        default_guild_settings = {"toggle": False}
        self.config.register_guild(**default_guild_settings)

    @commands.group(name='womp')
    async def womp_group(self, ctx):
        pass

    @womp_group.command(name='toggle')
    async def toggle_womp(self, ctx):
        current_state = await self.config.guild(ctx.guild).toggle()
        await self.config.guild(ctx.guild).toggle.set(not current_state)
        await ctx.send(f"Womp response is now {'enabled' if not current_state else 'disabled'}.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        guild_settings = await self.config.guild(message.guild).all()
        if guild_settings["toggle"] and "womp" in message.content.lower():
            random_amount = random.randint(1, 10)
            punctuation = random.choice(['.', '!', '?'])
            capitalization = random.choice([str.capitalize, str.upper])
            randomized_womp = ''.join([capitalization(char) if i % 2 == 0 else char for i, char in enumerate("womp" * random_amount)])
            
            response = f"{randomized_womp}{' ' * random_amount}{punctuation}"
            await message.channel.send(response)

def setup(bot):
    bot.add_cog(Womp(bot))
