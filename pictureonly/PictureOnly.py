import discord
from redbot.core import commands, Config, utils, checks, bot

class PictureOnly(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)
        default_guild_settings = {
            "picture_only_channel": None
        }
        self.config.register_guild(**default_guild_settings)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        guild_id = message.guild.id
        picture_only_channel = await self.config.guild(message.guild).picture_only_channel()

        if picture_only_channel and message.channel.id == picture_only_channel:
            if not message.attachments:
                await message.delete()

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def enable_picture_only(self, ctx):
        """Enables the picture-only mode in the current channel."""
        channel = ctx.channel
        await self.config.guild(ctx.guild).picture_only_channel.set(channel.id)
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send("The channel has been set to picture-only mode.")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def disable_picture_only(self, ctx):
        """Disables the picture-only mode in the current channel."""
        channel = ctx.channel
        await self.config.guild(ctx.guild).picture_only_channel.clear()
        await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send("The channel is no longer in picture-only mode.")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def set_picture_only_channel(self, ctx, channel: discord.TextChannel):
        """Sets the picture-only channel for the guild."""
        await self.config.guild(ctx.guild).picture_only_channel.set(channel.id)
        await ctx.send(f"The picture-only channel has been set to {channel.mention}.")

def setup(bot):
    bot.add_cog(PictureOnly(bot))
