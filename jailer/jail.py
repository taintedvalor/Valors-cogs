import asyncio
import discord
from discord import Embed, Message
from redbot.core import commands, Config, checks

class Jail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.original_roles = {}
        self.config = Config.get_conf(self, identifier=1234567890)
        default_guild_settings = {
            "allowed_role": None
        }
        self.config.register_guild(**default_guild_settings)

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
        self.original_roles[member.id] = member.roles
        await member.edit(roles=[], reason='Jailed')

        # Create and assign the jail role to the member
        jail_role = await ctx.guild.create_role(name='Jail Role', permissions=discord.Permissions(send_messages=True, read_messages=True))
        await member.add_roles(jail_role, reason='Jailed')

        # Set the jail text channel permissions
        await jail_channel.set_permissions(jail_role, send_messages=True, read_messages=True)
        allowed_role_id = await self.config.guild(ctx.guild).allowed_role()
        if allowed_role_id:
            allowed_role = discord.utils.get(ctx.guild.roles, id=allowed_role_id)
            if allowed_role:
                await jail_channel.set_permissions(allowed_role, send_messages=True, read_messages=True)
        else:
            await jail_channel.set_permissions(ctx.guild.default_role, read_messages=False)

        # Set the jail role permissions for other channels
        for channel in ctx.guild.channels:
            if channel != jail_channel:
                await channel.set_permissions(jail_role, send_messages=False, read_messages=False)

        await ctx.send(f'{member.mention} has been jailed.')

    @commands.command()
    @commands.has_permissions(manage_roles=True)
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

def setup(bot):
    bot.add_cog(Jail(bot))
