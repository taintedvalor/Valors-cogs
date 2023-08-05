import discord
from redbot.core import checks, commands
from redbot.core.utils.chat_formatting import warning, error, box

class UserDemoteCog(commands.Cog):
    """Demote a member and restrict their access."""

    def __init__(self, bot):
        self.bot = bot
        self.default_message_length = 60
        self.default_time_limit = 30 * 60  # 30 minutes in seconds
        self.restricted_members = {}

    @commands.group(name="userdemote", aliases=["udemote"], invoke_without_command=True)
    @checks.admin_or_permissions(manage_roles=True)
    async def userdemote_group(self, ctx):
        """Demote a member and restrict their access."""
        await ctx.send_help(ctx.command)

    @userdemote_group.command(name="demote")
    @checks.admin_or_permissions(manage_roles=True)
    async def userdemote_demote(self, ctx, member: discord.Member):
        """Demote a member and restrict their access to every channel."""
        # Get the "General" channel (you can change this as needed)
        general_channel = discord.utils.get(ctx.guild.text_channels, name="general")

        # Remove access to all channels
        for channel in ctx.guild.text_channels:
            await member.remove_roles(channel, reason="User Demoted")

        # Allow access to the "General" channel
        if general_channel:
            await member.add_roles(general_channel, reason="User Demoted")

        # Inform the member about the restriction
        await member.send(
            f"You have been demoted, and your access to all channels has been restricted except for {general_channel.mention}."
        )

        # Add the member to the restricted members dictionary
        self.restricted_members[member.id] = ctx.message.created_at.timestamp()

    @userdemote_group.command(name="configure")
    @checks.admin_or_permissions(manage_roles=True)
    async def userdemote_configure(self, ctx, message_length: int = None, time_limit: int = None):
        """Configure the user demote settings."""
        if message_length is not None:
            self.default_message_length = max(1, message_length)
        if time_limit is not None:
            self.default_time_limit = max(1, time_limit) * 60  # Convert to seconds

        await ctx.send(
            f"User demote settings updated.\n"
            f"Default Message Length: {self.default_message_length} characters\n"
            f"Default Time Limit: {self.default_time_limit // 60} minutes"
        )

    async def check_message_length(self, message: str):
        if len(message) > self.default_message_length:
            return False
        return True

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # Check if the member is restricted
        if message.author.id in self.restricted_members:
            time_diff = message.created_at.timestamp() - self.restricted_members[message.author.id]
            if time_diff >= self.default_time_limit:
                # Remove restrictions and allow sending the message
                self.restricted_members.pop(message.author.id)
            else:
                # Inform the member about the restriction and delete the message
                await message.author.send(
                    f"Your messaging is currently restricted. You can send a message every {self.default_time_limit // 60} minutes."
                )
                await message.delete()
                return

        if not await self.check_message_length(message.content):
            await message.channel.send(
                warning(
                    f"Your message exceeds the character limit of {self.default_message_length} characters."
                )
            )

def setup(bot):
    bot.add_cog(UserDemoteCog(bot))
