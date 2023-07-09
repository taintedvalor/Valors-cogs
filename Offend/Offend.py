from redbot.core import commands, Config
import discord

class Offend(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)
        self.default_config = {
            "reaction_emoji": "🖕",  # Default reaction emoji
            "active_users": []  # List of active users
        }
        self.config.register_guild(**self.default_config)

    @commands.group(name="offend")
    async def offend_group(self, ctx):
        """Manage offend settings."""
        pass

    @offend_group.command(name="activate")
    async def activate_offend(self, ctx):
        """Activate offend reactions for the mentioned user."""
        mentioned_users = ctx.message.mentions
        if not mentioned_users:
            await ctx.send("Please mention a user to activate offend reactions.")
            return

        active_users = await self.config.guild(ctx.guild).active_users()
        for user in mentioned_users:
            if user.id not in active_users:
                active_users.append(user.id)
        await self.config.guild(ctx.guild).active_users.set(active_users)
        await ctx.send("Offend reactions activated.")

    @offend_group.command(name="deactivate")
    async def deactivate_offend(self, ctx):
        """Deactivate offend reactions for the mentioned user."""
        mentioned_users = ctx.message.mentions
        if not mentioned_users:
            await ctx.send("Please mention a user to deactivate offend reactions.")
            return

        active_users = await self.config.guild(ctx.guild).active_users()
        for user in mentioned_users:
            if user.id in active_users:
                active_users.remove(user.id)
        await self.config.guild(ctx.guild).active_users.set(active_users)
        await ctx.send("Offend reactions deactivated.")

    @offend_group.command(name="reactionemoji")
    async def set_reaction_emoji(self, ctx, emoji: str):
        """Set the reaction emoji."""
        await self.config.guild(ctx.guild).reaction_emoji.set(emoji)
        await ctx.send(f"Reaction emoji set to {emoji}.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        guild = message.guild
        active_users = await self.config.guild(guild).active_users()
        reaction_emoji = await self.config.guild(guild).reaction_emoji()

        if message.author.id in active_users:
            await message.add_reaction(reaction_emoji)

def setup(bot):
    bot.add_cog(Offend(bot))
