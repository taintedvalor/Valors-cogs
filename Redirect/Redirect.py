import discord
from redbot.core import commands, Config


class CommandRedirect(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=123456789)  # Replace with a unique identifier
        default_guild_settings = {
            "command_channel": None
        }
        self.config.register_guild(**default_guild_settings)

    @commands.Cog.listener()
    async def on_command(self, ctx):
        if not await self._is_command_channel(ctx.guild, ctx.channel):
            await ctx.send("Commands can only be run in the commands channel.")
            await ctx.message.delete()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            if not await self._is_command_channel(ctx.guild, ctx.channel):
                await ctx.send("Commands can only be run in the commands channel.")
                await ctx.message.delete()

    async def _is_command_channel(self, guild, channel):
        command_channel = await self.config.guild(guild).command_channel()
        return command_channel is None or channel.id == command_channel

    @commands.group(name="commandchannel")
    @commands.guild_only()
    @commands.admin()
    async def command_channel_group(self, ctx):
        """Command to manage the command channel."""

    @command_channel_group.command(name="set")
    async def set_command_channel(self, ctx, channel: discord.TextChannel):
        """Set the command channel for the guild."""
        await self.config.guild(ctx.guild).command_channel.set(channel.id)
        await ctx.send(f"Command channel set to {channel.mention}.")

    @command_channel_group.command(name="clear")
    async def clear_command_channel(self, ctx):
        """Clear the command channel for the guild."""
        await self.config.guild(ctx.guild).command_channel.clear()
        await ctx.send("Command channel cleared.")


def setup(bot):
    bot.add_cog(CommandRedirect(bot))
