from redbot.core import commands, Config
import discord

class Offend(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)
        self.default_global_config = {
            "global_reaction_emoji": "🖕"  # Default global reaction emoji
        }
        self.default_user_config = {
            "personal_reaction_emoji": "",  # Default personal reaction emoji
            "active": False  # Offend reactions active status
        }
        self.config.register_global(**self.default_global_config)
        self.config.register_user(**self.default_user_config)

    @commands.group(name="offend")
    async def offend_group(self, ctx):
        """Manage offend settings."""
        pass

    @offend_group.command(name="globalreactionemoji")
    async def set_global_reaction_emoji(self, ctx, emoji: str):
        """Set the global reaction emoji."""
        await self.config.global_reaction_emoji.set(emoji)
        await ctx.send(f"Global reaction emoji set to {emoji}.")

    @offend_group.command(name="personalreactionemoji")
    async def set_personal_reaction_emoji(self, ctx, emoji: str):
        """Set the personal reaction emoji."""
        await self.config.user(ctx.author).personal_reaction_emoji.set(emoji)
        await ctx.send(f"Personal reaction emoji set to {emoji}.")

    @offend_group.command(name="activate")
    async def activate_offend(self, ctx):
        """Activate offend reactions for the mentioned user."""
        mentioned_users = ctx.message.mentions
        if not mentioned_users:
            await ctx.send("Please mention a user to activate offend reactions.")
            return

        for user in mentioned_users:
            await self.config.user(user).active.set(True)
        await ctx.send("Offend reactions activated.")

    @offend_group.command(name="deactivate")
    async def deactivate_offend(self, ctx):
        """Deactivate offend reactions for the mentioned user."""
        mentioned_users = ctx.message.mentions
        if not mentioned_users:
            await ctx.send("Please mention a user to deactivate offend reactions.")
            return

        for user in mentioned_users:
            await self.config.user(user).active.set(False)
        await ctx.send("Offend reactions deactivated.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        guild = message.guild
        global_reaction_emoji = await self.config.global_reaction_emoji()
        user_config = self.config.user(message.author)
        personal_reaction_emoji = await user_config.personal_reaction_emoji()
        active = await user_config.active()

        if active:
            if personal_reaction_emoji:
                await message.add_reaction(personal_reaction_emoji)
            else:
                await message.add_reaction(global_reaction_emoji)

def setup(bot):
    bot.add_cog(Offend(bot))
