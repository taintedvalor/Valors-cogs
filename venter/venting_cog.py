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
    @checks.admin_or_permissions(manage_guild=True)
    async def set_venting_channel(self, ctx, channel: discord.TextChannel):
        """Set the venting channel for the guild."""
        guild = ctx.guild
        await self.bot.set_cog_data(guild, "vent_channel", channel.id)
        await ctx.send(f"The venting channel has been set to {channel.mention}.")

    @commands.command(pass_context=True, rest_is_raw=True)
    async def vent(self, ctx, *, message: str = None):
        """Vent anonymously in the venting channel for the guild."""
        guild = ctx.guild
        vent_channel_id = await self.bot.get_cog_data(guild, "vent_channel")
        if not vent_channel_id:
            return await ctx.send("The venting channel has not been set for this guild.")

        vent_channel = guild.get_channel(vent_channel_id)
        if not vent_channel:
            return await ctx.send("The venting channel is invalid or no longer exists.")

        attachments = ctx.message.attachments
        if not message and not attachments:
            return await ctx.send("Please provide a message or an attachment.")

        vent_message = f"Anonymous Person:\n{message}" if message else "Anonymous Person"
        files = [await attachment.to_file(spoiler=is_image_spoiler(attachment.filename)) for attachment in attachments]
        await vent_channel.send(content=vent_message, files=files)
        await ctx.send("Your message has been sent.")

def is_image_spoiler(filename: str) -> bool:
    image_extensions = [".png", ".jpg", ".jpeg", ".gif"]
    return any(filename.lower().endswith(ext) for ext in image_extensions)

def setup(bot):
    bot.add_cog(VentCog(bot))
