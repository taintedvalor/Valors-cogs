import asyncio
from discord import Embed, Message
from redbot.core import commands, Config, checks

class Jail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def jail(self, ctx, member: discord.Member):
        # Create the jail category if it doesn't exist
        jail_category = discord.utils.get(ctx.guild.categories, name='Jail')
        if not jail_category:
            jail_category = await ctx.guild.create_category('Jail')

        # Create the jail text channel
        jail_channel = await jail_category.create_text_channel('jail')

        # Remove all roles from the member
        original_roles = member.roles
        await member.edit(roles=[], reason='Jailed')

        # Create and assign the jail role to the member
        jail_role = await ctx.guild.create_role(name='Jail Role', permissions=discord.Permissions.none())
        await member.add_roles(jail_role, reason='Jailed')

        # Set the jail text channel permissions
        await jail_channel.set_permissions(member, read_messages=True, send_messages=True)
        await jail_channel.set_permissions(jail_role, read_messages=True, send_messages=True)

        await ctx.send(f'{member.mention} has been jailed.')

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unjail(self, ctx, member: discord.Member):
        # Find the jail category and jail role
        jail_category = discord.utils.get(ctx.guild.categories, name='Jail')
        jail_role = discord.utils.get(ctx.guild.roles, name='Jail Role')

        # Retrieve the original roles of the member
        original_roles = member.roles

        # Remove the jail role from the member
        await member.remove_roles(jail_role, reason='Unjailed')

        # Restore the original roles to the member
        await member.edit(roles=original_roles, reason='Unjailed')

        # Delete the jail text channel
        jail_channel = discord.utils.get(jail_category.channels, name='jail')
        await jail_channel.delete()

        await ctx.send(f'{member.mention} has been unjailed.')

@commands.is_owner()
@commands.group()
async def jailsetup(self, ctx):
    """Set up the jail category and role."""
    if ctx.invoked_subcommand is None:
        await ctx.send_help()

@jailsetup.command(name="create")
async def jailsetup_create(self, ctx):
    """Create the jail category and role."""
    guild = ctx.guild

    # Create the jail category if it doesn't exist
    jail_category = discord.utils.get(guild.categories, name='Jail')
    if not jail_category:
        await guild.create_category('Jail')

    # Create the jail role if it doesn't exist
    jail_role = discord.utils.get(guild.roles, name='Jail Role')
    if not jail_role:
        permissions = discord.Permissions.none()
        await guild.create_role(name='Jail Role', permissions=permissions)

    await ctx.send("Jail category and role created.")

def setup(bot):
    bot.add_cog(Jail(bot))

