import discord
from redbot.core import commands

class ArmyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='army')
    async def army_group(self, ctx):
        """Manage army-related commands."""
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid army command. Use `help army` for more information.')

    @army_group.command(name='rename_all')
    async def rename_all_members(self, ctx, *, new_name):
        """Rename all members in the guild."""
        for member in ctx.guild.members:
            try:
                await member.edit(nick=new_name)
            except discord.Forbidden:
                print(f"Unable to rename {member.display_name}")

    @army_group.command(name='reset_names')
    async def reset_all_names(self, ctx):
        """Reset the nicknames of all members in the guild."""
        for member in ctx.guild.members:
            try:
                await member.edit(nick=None)
            except discord.Forbidden:
                print(f"Unable to reset nickname for {member.display_name}")

def setup(bot):
    bot.add_cog(Army(bot))
