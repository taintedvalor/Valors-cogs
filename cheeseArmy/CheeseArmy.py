import discord
from redbot.core import commands, Config

class CheeseArmy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=123456789)  # Change identifier to your cog's unique identifier

    @commands.command()
    async def cheesearmy_rename(self, ctx, new_name: str):
        """Rename all users in the guild with the specified name."""
        async with self.config.guild(ctx.guild).usernames() as usernames:
            for member in ctx.guild.members:
                usernames[member.id] = member.display_name
                await member.edit(nick=new_name)

    @commands.command()
    async def cheesearmy_restorenames(self, ctx):
        """Remove nicknames from all users."""
        async with self.config.guild(ctx.guild).usernames() as usernames:
            for member in ctx.guild.members:
                old_name = usernames.get(member.id, None)
                if old_name is not None:
                    await member.edit(nick=None)
                    del usernames[member.id]

# Make sure to add this cog to the bot in your main script
bot.add_cog(CheeseArmy(bot))
