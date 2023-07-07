import asyncio
import discord
from discord import Embed, Message
from redbot.core import commands, Config, checks


class Jail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.original_roles = {}
        self.create_channel_role = True

    @commands.group()
    @commands.has_permissions(manage_roles=True)
    async def jailer(self, ctx):
        """Parent command for jail-related actions."""
        if ctx.invoked_subcommand is None:
            await ctx.send_help()

    @jailer.command()
    async def toggle_create(self, ctx):
        """Toggle the creation and deletion of jail category, text channel, and role."""
        self.create_channel_role = not self.create_channel_role
        status = "enabled" if self.create_channel_role else "disabled"
        await ctx.send(f"Creation and deletion of jail category, text channel, and role is now {status}.")

    @jailer.command()
    async def jail(self, ctx, member: discord.Member):
        if self.create_channel_role:
            # Check if jail category and jail text channel exist
            jail_category = discord.utils.get(ctx.guild.categories, name='Jail')
            if not jail_category:
                await ctx.send("Please create the 'Jail' category before jailing someone.")
                return

            jail_channel = discord.utils.get(jail_category.channels, name='jail')
            if not jail_channel:
                await ctx.send("Please create the 'jail' text channel under the 'Jail' category before jailing someone.")
                return

        # Remove all roles from the member
        self.original_roles[member.id] = member.roles
        await member.edit(roles=[], reason='Jailed')

        if self.create_channel_role:
            # Create and assign the jail role to the member
            jail_role = await ctx.guild.create_role(name='Jail Role', permissions=discord.Permissions(send_messages=True, read_messages=True))
            await member.add_roles(jail_role, reason='Jailed')

            # Set the jail role permissions for other channels
            for channel in ctx.guild.channels:
                if channel != jail_channel:
                    await channel.set_permissions(jail_role, send_messages=False, read_messages=False)

        await ctx.send(f'{member.mention} has been jailed.')

    @jailer.command()
    async def unjail(self, ctx, member: discord.Member):
        if self.create_channel_role:
            # Check if jail category and jail role exist
            jail_category = discord.utils.get(ctx.guild.categories, name='Jail')
            jail_role = discord.utils.get(ctx.guild.roles, name='Jail Role')

            if not jail_category or not jail_role:
                await ctx.send("Cannot unjail someone as the jail category or jail role is missing.")
                return

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

                # Delete the jail role
                await jail_role.delete()

                # Delete the jail category if no channels remain
                if len(jail_category.channels) == 0:
                    await jail_category.delete()

                await ctx.send(f'{member.mention} has been unjailed.')
            else:
                await ctx.send(f'{member.mention} is not currently jailed.')
        else:
            await ctx.send("Creation and deletion of jail category, text channel, and role is disabled.")


def setup(bot):
    bot.add_cog(Jail(bot))
