import discord
from redbot.core import commands, Config


class CommandRedirect(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=123456789)  # Replace with a unique identifier
        default_guild_settings = {
            "command_channels": []
        }
        self.config.register_guild(**default_guild_settings)

    @commands.Cog.listener()
    async def on_command(self, ctx):
        if not await self._is_command_channel(ctx.guild, ctx.channel):
            notice_message = await ctx.send("Commands can only be run in the command channels.")
            await ctx.message.delete()
            await self._delete_messages(ctx.channel, [notice_message, ctx.message], 2)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            if not await self._is_command_channel(ctx.guild, ctx.channel):
                notice_message = await ctx.send("Commands can only be run in the command channels.")
                await ctx.message.delete()
                await self._delete_messages(ctx.channel, [notice_message, ctx.message], 2)

    async def _is_command_channel(self, guild, channel):
        command_channels = await self.config.guild(guild).command_channels()
        return not command_channels or channel.id in command_channels

    async def _delete_messages(self, channel, messages, count):
        try:
            async for message in channel.history(limit=count):
                if message in messages:
                    continue
                await message.delete()
        except discord.Forbidden:
            pass

    @commands.group(name="commandchannel")
    @commands.guild_only()
    @commands.admin()
    async def command_channel_group(self, ctx):
        """Command to manage the command channels."""

    @command_channel_group.command(name="add")
    async def add_command_channel(self, ctx, channel: discord.TextChannel):
        """Add a command channel for the guild."""
        command_channels = await self.config.guild(ctx.guild).command_channels()
        if channel.id in command_channels:
            await ctx.send(f"{channel.mention} is already a command channel.")
            return
        command_channels.append(channel.id)
        await self.config.guild(ctx.guild).command_channels.set(command_channels)
        await ctx.send(f"{channel.mention} has been added as a command channel.")

    @command_channel_group.command(name="remove")
    async def remove_command_channel(self, ctx, channel: discord.TextChannel):
        """Remove a command channel from the guild."""
        command_channels = await self.config.guild(ctx.guild).command_channels()
        if channel.id not in command_channels:
            await ctx.send(f"{channel.mention} is not a command channel.")
            return
        command_channels.remove(channel.id)
        await self.config.guild(ctx.guild).command_channels.set(command_channels)
        await ctx.send(f"{channel.mention} has been removed as a command channel.")

    @command_channel_group.command(name="list")
    async def list_command_channels(self, ctx):
        """List all command channels for the guild."""
        command_channels = await self.config.guild(ctx.guild).command_channels()
        if not command_channels:
            await ctx.send("No command channels set for this guild.")
            return
        channel_mentions = [ctx.guild.get_channel(cid).mention for cid in command_channels]
        await ctx.send(f"Command channels for this guild: {', '.join(channel_mentions)}")


def setup(bot):
    bot.add_cog(CommandRedirect(bot))
