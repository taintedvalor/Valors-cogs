import asyncio
from discord import Embed, Message
from redbot.core import commands, Config, checks

import discord
from discord.ext import commands

class Jail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.jail_role_name = "Jail"  # Customize the jail role name here
        self.jail_category_name = "Jail Category"  # Customize the jail category name here
        self.jail_overwrite = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        self.jail_channel = None
        self.user_roles = {}

    async def give_jail_role(self, user):
        guild = user.guild
        jail_role = discord.utils.get(guild.roles, name=self.jail_role_name)

        if not jail_role:
            jail_role = await guild.create_role(name=self.jail_role_name)

        self.user_roles[user.id] = [role.id for role in user.roles]
        await user.add_roles(jail_role)

        jail_category = discord.utils.get(guild.categories, name=self.jail_category_name)
        if not jail_category:
            jail_category = await guild.create_category(name=self.jail_category_name)

        self.jail_channel = await guild.create_text_channel(name="jail", category=jail_category)
        await self.jail_channel.set_permissions(jail_role, overwrite=self.jail_overwrite)
        await user.move_to(self.jail_channel)

        # Send DM to the user
        await user.send("You have been jailed.")

    async def remove_jail_role(self, user):
        guild = user.guild
        jail_role = discord.utils.get(guild.roles, name=self.jail_role_name)

        if jail_role:
            await user.remove_roles(jail_role)

        if self.jail_channel:
            await self.jail_channel.delete()
            self.jail_channel = None

        await user.move_to(None)

        if user.id in self.user_roles:
            role_ids = self.user_roles[user.id]
            roles = [guild.get_role(role_id) for role_id in role_ids]
            await user.add_roles(*roles)

            del self.user_roles[user.id]

        # Send DM to the user
        await user.send("You have been unjailed.")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def jail(self, ctx, user: discord.Member):
        await self.give_jail_role(user)
        await ctx.send(f"{user.mention} has been jailed.")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unjail(self, ctx, user: discord.Member):
        await self.remove_jail_role(user)
        await ctx.send(f"{user.mention} has been unjailed.")

def setup(bot):
    bot.add_cog(Jail(bot))

