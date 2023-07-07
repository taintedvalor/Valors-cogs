import asyncio
import discord
from discord import Embed, Message
from redbot.core import commands, Config, checks

class Jail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.original_roles = {}
        self.allowed_roles = []  # List of role IDs allowed to access jail channel

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
        jail_role = await ctx.guild.create_role(name='Jail Role')
        await member.add_roles(jail_role, reason='Jailed')

        # Set the jail role permissions
        for channel in ctx.guild.channels:
            if isinstance(channel, discord.TextChannel) and channel == jail_channel:
                await channel.set_permissions(jail_role, read_messages=False, send_messages=False)

        # Set the jail channel permissions
        for role in ctx.guild.roles:
            if role.id in self.allowed_roles or role == jail_role:
                await jail_channel.set_permissions(role, read_messages=True, send_messages=True)

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

            # Delete the jail role
            await jail_role.delete()

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

    @jailer.command(name="allow")
    async def jailer_allow(self, ctx, role: discord.Role):
        """Allow a role to access the jail channel."""
        if role.id not in self.allowed_roles:
            self.allowed_roles.append(role.id)
            await ctx.send(f"{role.name} is now allowed to access the jail channel.")
        else:
            await ctx.send(f"{role.name} is already allowed to access the jail channel.")

    @jailer.command(name="remove")
    async def jailer_remove(self, ctx, role: discord.Role):
        """Remove a role from the allowed list to access the jail channel."""
        if role.id in self.allowed_roles:
            self.allowed_roles.remove(role.id)
            await ctx.send(f"{role.name} is no longer allowed to access the jail channel.")
        else:
            await ctx.send(f"{role.name} is not currently allowed to access the jail channel.")

def setup(bot):
    bot.add_cog(Jail(bot))

