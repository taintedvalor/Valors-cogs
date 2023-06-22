import discord
from redbot.core import commands, checks

class Venting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def vent(self, ctx, *, vent_text):
        """Vent anonymously in a designated channel."""
        vent_channel = await self.get_venting_channel(ctx.author)
        if vent_channel is None:
            await ctx.send("No venting channel found. Please contact the bot administrator.")
            return

        guild = vent_channel.guild
        message = f"Anonymous Vent:\n\n{vent_text}"

        try:
            await vent_channel.send(message)
            await ctx.send("Your vent has been posted anonymously.")
        except discord.Forbidden:
            await ctx.send("I don't have permission to send messages in the venting channel.")

    async def get_venting_channel(self, user):
        """Retrieve the venting channel for the user's selected guild."""
        # Implement your own logic to retrieve the venting channel based on user selection.
        # This could involve storing guild-channel mappings in a database or configuration file.
        # For simplicity, let's assume the venting channel is stored in the bot's cog settings.

        venting_channels = await self.bot.get_cog("Core").get_vent_cog_settings()
        guild_id = await self.prompt_user_for_guild(user, venting_channels)

        if guild_id:
            return venting_channels.get(str(guild_id))

    async def prompt_user_for_guild(self, user, venting_channels):
        """Prompt the user to select a guild for venting."""
        dm_channel = user.dm_channel or await user.create_dm()

        guild_list = [
            f"{index}. {guild.name}"
            for index, guild in enumerate(user.mutual_guilds, start=1)
        ]

        if not guild_list:
            await dm_channel.send("You are not in any mutual guilds with the bot.")
            return None

        await dm_channel.send("Please select a guild number for venting:\n" + "\n".join(guild_list))

        def check(message):
            return (
                message.author == user
                and message.channel == dm_channel
                and message.content.isdigit()
            )

        try:
            message = await self.bot.wait_for("message", check=check, timeout=60)
            guild_index = int(message.content) - 1
            guild = user.mutual_guilds[guild_index]
            return guild.id
        except (ValueError, asyncio.TimeoutError):
            await dm_channel.send("Invalid selection or timeout.")
            return None
