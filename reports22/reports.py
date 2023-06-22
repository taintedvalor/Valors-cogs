import logging
import asyncio
from typing import List, Literal, Union
from datetime import timedelta
from copy import copy
import contextlib
import discord

from redbot.core import Config, commands
from redbot.core.utils import AsyncIter
from redbot.core.utils.chat_formatting import pagify, box
from redbot.core.utils.antispam import AntiSpam
from redbot.core.bot import Red
from redbot.core.i18n import Translator, cog_i18n, set_contextual_locales_from_guild
from redbot.core.utils.predicates import MessagePredicate
from redbot.core.utils.tunnel import Tunnel

class VentCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def vent(self, ctx, guild_id: int, *, message):
        guild = self.bot.get_guild(guild_id)
        if guild is None:
            await ctx.send("Invalid guild ID.")
            return

        channel_name = "venting"
        channel = discord.utils.get(guild.channels, name=channel_name, type=discord.ChannelType.text)
        if channel is None:
            await ctx.send("Invalid channel name.")
            return

        forwarded_message = f"**{ctx.author.display_name}**: {message}"
        await channel.send(forwarded_message)
        await ctx.send("Your message has been forwarded to the venting channel.")

def setup(bot):
    bot.add_cog(VentCog(bot))
