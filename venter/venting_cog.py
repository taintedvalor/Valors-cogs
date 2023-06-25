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

    @commands.command(pass_context=True, rest_is_raw=True)
    async def vent(self, ctx, guild_id: int, *, message: str = None):
        """Vent Anonymously from Dms to a specific guild in a 🌬-venting-room"""
        target_guild = self.bot.get_guild(guild_id)
        if not target_guild:
            return await ctx.send("Target guild not found.")

        target_channel = discord.utils.get(target_guild.text_channels, name="🌬-venting-room")
        if not target_channel:
            return await ctx.send("No ventingroom channel in the given guild.")

        attachments = ctx.message.attachments
        if not message and not attachments:
            return await ctx.send("Please provide a message or an attachment.")

        vent_message = f"Anonymous Person:\n{message}" if message else "Anonymous Person"
        await target_channel.send(content=vent_message, files=[await attachment.to_file() for attachment in attachments])
        await ctx.send("Your message has been sent.")

def setup(bot):
    bot.add_cog(VentCog(bot))

