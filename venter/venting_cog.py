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

    @commands.group(pass_context=True, invoke_without_command=True)
    async def vent(self, ctx):
        """Venting commands."""
        pass

    @vent.command()
    async def setchannel(self, ctx, channel: discord.TextChannel):
        """Set the venting channel for this guild."""
        await self.bot.set_cog_settings(self, ctx.guild, channel.id)
        await ctx.send(f"Venting channel set to {channel.mention}.")

    @commands.command(pass_context=True, rest_is_raw=True)
    async def send(self, ctx, *, message: str = None):
        """Send an anonymous vent message to the configured venting channel."""
        vent_channel_id = await self.bot.get_cog_settings(self, ctx.guild, default=None)
        if vent_channel_id is None:
            return await ctx.send("No venting channel set for this guild. Use the `vent setchannel` command.")

        vent_channel = ctx.guild.get_channel(vent_channel_id)
        if not vent_channel:
            return await ctx.send("The configured venting channel is invalid or not found.")

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
