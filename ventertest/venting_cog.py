import discord
from redbot.core import commands, checks, bot
from random import choice as randchoice
from pprint import pprint as pp
from typing import List, Dict
from fuzzywuzzy import process

BaseCog = getattr(commands, "Cog", object)


class VentCog(commands.Cog):
    def __init__(self, bot_instance: bot):
        self.bot = bot_instance
        """Cog for venting Anonymously in dms"""

    @commands.command(pass_context=True, rest_is_raw=True)
    async def set_venting_channel(self, ctx, guild_id: int, channel_name: str):
        """Set the venting channel in a specific guild"""
        target_guild = self.bot.get_guild(guild_id)
        if not target_guild:
            return await ctx.send("Target guild not found.")

        target_channel = discord.utils.get(target_guild.text_channels, name=channel_name)
        if not target_channel:
            return await ctx.send("Target channel not found.")

        await ctx.send(f"Venting channel set to '{channel_name}' in guild '{target_guild.name}'.")

    @commands.command(pass_context=True, rest_is_raw=True)
    async def vent(self, ctx, guild_id: int, *, message: str):
        """Vent Anonymously from Dms to a specific guild's venting channel"""
        target_guild = self.bot.get_guild(guild_id)
        if not target_guild:
            return await ctx.send("Target guild not found.")

        target_channel = discord.utils.get(target_guild.text_channels, name="ventingroom")
        if not target_channel:
            return await ctx.send("No ventingroom channel set in the given guild.")

        await target_channel.send(f"Anonymous Person: {message}")
        await ctx.send("Your message has been Sent.")


def setup(bot):
    bot.add_cog(VentCog(bot))
