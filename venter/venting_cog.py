import discord
from redbot.core import commands, bot
from typing import List, Dict
from fuzzywuzzy import process

BaseCog = getattr(commands, "Cog", object)

class VentCog(commands.Cog):
    def __init__(self, bot_instance: bot):
        self.bot = bot_instance
        self.config = bot_instance.get_cog("Config")  # Assuming you have a Config cog, replace it with the actual name if different

    @commands.group(aliases=["v"], invoke_without_command=True)
    async def venter(self, ctx):
        """Parent command for venting-related commands."""
        await ctx.send_help(ctx.command)

    @venter.command()
    @commands.guild_only()
    @commands.admin_or_permissions(manage_channels=True)
    async def set_venting_channel(self, ctx, channel: discord.TextChannel):
        """Set the venting channel for the guild."""
        await self.config.guild(ctx.guild).venting_channel.set(channel.id)
        await ctx.send(f"Venting channel set to {channel.mention}.")

    @venter.command(pass_context=True, rest_is_raw=True, aliases=["v"])
    async def vent(self, ctx, guild: str, *, message: str = None):
        """Vent anonymously in the venting channel of a specified guild."""
        venting_channel_id = await self.get_venting_channel(guild)
        if not venting_channel_id:
            return await ctx.send("Venting channel is not set for the specified guild.")

        venting_channel = self.bot.get_channel(venting_channel_id)
        if not venting_channel:
            return await ctx.send("Venting channel not found in the specified guild.")

        attachments = ctx.message.attachments
        if not message and not attachments:
            return await ctx.send("Please provide a message or an attachment.")

        vent_message = f"Anonymous Person:\n{message}" if message else "Anonymous Person"
        files = [await attachment.to_file(spoiler=is_image_spoiler(attachment.filename)) for attachment in attachments]

        if vent_message:
            await venting_channel.send(content=vent_message, files=files)
        else:
            for file in files:
                await venting_channel.send(file=file)

        await ctx.send("Your message has been sent.")

    async def get_venting_channel(self, guild: str) -> int:
        guild_id = None
        try:
            guild_id = int(guild)
        except ValueError:
            pass

        venting_channel_id = None
        if guild_id:
            venting_channel_id = await self.config.guild_from_id(guild_id).venting_channel()
        else:
            guild = discord.utils.find(lambda g: g.name.lower() == guild.lower(), self.bot.guilds)
            if guild:
                venting_channel_id = await self.config.guild(guild).venting_channel()

        return venting_channel_id

def is_image_spoiler(filename: str) -> bool:
    image_extensions = [".png", ".jpg", ".jpeg", ".gif"]
    return any(filename.lower().endswith(ext) for ext in image_extensions)

def setup(bot):
    bot.add_cog(VentCog(bot))
