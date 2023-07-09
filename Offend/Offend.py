from redbot.core import commands, Config
import discord
import asyncio

class Offend(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)
        self.default_config = {
            "reaction_time": 10,  # Default reaction time in seconds
            "reaction_emoji": "🖕"  # Default reaction emoji
        }
        self.config.register_guild(**self.default_config)

    @commands.group(name="offend")
    async def offend_group(self, ctx):
        """Manage offend settings."""
        pass

    @offend_group.command(name="reactiontime")
    async def set_reaction_time(self, ctx, time: int):
        """Set the reaction time in seconds."""
        if time <= 0:
            await ctx.send("Reaction time must be a positive number.")
            return
        await self.config.guild(ctx.guild).reaction_time.set(time)
        await ctx.send(f"Reaction time set to {time} seconds.")

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
        reaction_time = await self.config.guild(guild).reaction_time()
        reaction_emoji = await self.config.guild(guild).reaction_emoji()

        if reaction_time > 0:
            mentioned_users = message.mentions
            for user in mentioned_users:
                await message.add_reaction(reaction_emoji)
                await asyncio.sleep(reaction_time)
                await message.remove_reaction(reaction_emoji, self.bot.user)
                await asyncio.sleep(0.5)  # Sleep for a short duration to avoid rate limits

def setup(bot):
    bot.add_cog(Offend(bot))
