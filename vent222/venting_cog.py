import asyncio
import re
import random
from datetime import datetime, timedelta
from typing import Iterable, List, Mapping, Tuple, Dict, Set, Literal, Union
from urllib.parse import quote_plus

import discord
from rapidfuzz import process

from redbot.core import Config, commands
from redbot.core.commands import Parameter
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils import menus, AsyncIter
from redbot.core.utils.chat_formatting import box, pagify, escape, humanize_list
from redbot.core.utils.predicates import MessagePredicat

class VentCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def vent(self, ctx, guild_id: int, *, message):
        guild = self.bot.get_guild(guild_id)
        if guild is None:
            await ctx.send("Target guild not found.")
            return

        channel = discord.utils.get(guild.channels, name="venting")
        if channel is None:
            await ctx.send("Target channel not found.")
            return

        try:
            await channel.send(f"Vent from {ctx.author.name}: {message}")
            await ctx.send("Message vented successfully!")
        except discord.Forbidden:
            await ctx.send("Bot doesn't have permission to send messages in the target channel.")
        except discord.HTTPException:
            await ctx.send("An error occurred while venting the message. Please try again later.")

def setup(bot):
    bot.add_cog(VentCog(bot))
