import discord
from redbot.core import commands, checks, bot
from random import choice as randchoice
from pprint import pprint as pp

from typing import List, Dict

from fuzzywuzzy import process

class VentCog(commands.Cog):
    """Cog for venting messages"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def vent(self, ctx, guild_id: int, *, message: str):
        """Forward a message to a specific guild and channel"""
        target_guild = self.bot.get_guild(guild_id)
        if not target_guild:
            return await ctx.send("Target guild not found.")

        target_channel = discord.utils.get(target_guild.text_channels, name="ventroom")
        if not target_channel:
            return await ctx.send("Target channel not found.")

        await target_channel.send(f"Message from {ctx.author.name}: {message}")
        await ctx.send("Your message has been forwarded.")

def setup(bot):
    bot.add_cog(VentCog(bot))
