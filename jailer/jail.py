import asyncio
import discord
from discord import Embed, Message
from redbot.core import commands, Config, checks

class Jail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.original_roles = {}
        self.allowed_roles = []  # List of role names allowed to access jail channel

    @commands.group()
    @commands.has_permissions(manage_roles=True)
    async def jailer(self, ctx):
        """Jail management commands."""
        if ctx.invoked_subcommand is None:
            await ctx.send_help()

    @jailer.command(name="jail")
    async def jail(self, ctx, member: discord.Member):
        # Create the jail category if it doesn't exist
        jail_category = discord.utils.get(ctx.guild.categories, name='Jail')
        if not jail_category:
            jail_category = await ctx.guild.create_category('Jail')

        # Create the jail text channel
        jail_channel = await jail_category.create_text_channel('jail')

        # Remove all roles from the member
        self.original_roles[member.id] = member.roles
        await member.edit(roles=[], reason='Jailed')

        # Create and assign the jail role to the member
        jail_role = await ctx.guild.create_role(name='Jail Role', permissions=discord.Permissions(send_messages=True, read_messages=True))
        await member.add_roles(jail_role, reason='Jailed')

        # Set the jail text channel permissions
        await jail_channel.set_permissions(jail_role, send_messages=True, read_messages=True)

        # Set the jail role permissions for other channels
        for channel in ctx.guild.channels:
            if channel != jail_channel:
                await channel.set_permissions(jail_role, send_messages=False, read_messages=False)

        await ctx.send(f'{member.mention} has been jailed.')

    @jailer.command(name="unjail")
    async def unjail(self, ctx, member: discord.Member):
        # Find the jail category and jail role
        jail_category = discord.utils.get(ctx.guild.categories, name='Jail')
        jail_role = discord.utils.get(ctx.guild.roles, name='Jail Role')

        # Retrieve the original roles of the member
        original_roles = self.original_roles.get(member.id)

        if original_roles:
            # Remove the jail role from the member
            await member.remove_roles(jail_role, reason='Unjailed')

            # Restore the original roles to the member
            await member.edit(roles=original_roles, reason='Unjailed')

            # Delete the jail text channel
            jail_channel = discord.utils.get(jail_category.channels, name='jail')
            await jail_channel.delete()

            # Delete the jail category if no channels remain
            if len(jail_category.channels) == 0:
                await jail_category.delete()

            await ctx.send(f'{member.mention} has been unjailed.')
        else:
            await ctx.send(f'{member.mention} is not currently jailed.')

    @jailer.command(name="setup")
    @commands.is_owner()
    async def jailer_setup(self, ctx):
        """Create the jail category and role."""
        guild = ctx.guild

        # Create the jail category if it doesn't exist
        jail_category = discord.utils.get(guild.categories, name='Jail')
        if not jail_category:
            await guild.create_category('Jail')

        # Create the jail role if it doesn't exist
        jail_role = discord.utils.get(guild.roles, name='Jail Role')
        if not jail_role:
            permissions = discord.Permissions(send_messages=True, read_messages=True)
            await guild.create_role(name='Jail Role', permissions=permissions)

        await ctx.send("Jail category and role created.")

    @jailer.command(name="allow")
    async def jailer_allow(self, ctx, role: discord.Role):
        """Allow a role to access the jail channel."""
        if role.name not in self.allowed_roles:
            self.allowed_roles.append(role.name)
            await ctx.send(f"{role.name} is now allowed to access the jail channel.")
        else:
            await ctx.send(f"{role.name} is already allowed to access the jail channel.")

    @jailer.command(name="disallow")
    async def jailer_disallow(self, ctx, role: discord.Role):
        """Disallow a role from accessing the jail channel."""
        if role.name in self.allowed_roles:
            self.allowed_roles.remove(role.name)
            await ctx.send(f"{role.name} is no longer allowed to access the jail channel.")
        else:
            await ctx.send(f"{role.name} is not currently allowed to access the jail channel.")

def setup(bot):
    bot.add_cog(Jail(bot))
