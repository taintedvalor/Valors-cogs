from redbot.core import commands, Config
import discord


class WardenCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)  # Replace with a unique identifier
        self.config.register_guild(jail_role=None)
        self.original_roles = {}

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def configjailrole(self, ctx, role: discord.Role):
        await self.config.guild(ctx.guild).jail_role.set(role.id)
        await ctx.send(f"Jail role configured as {role.name}.")

    @commands.command()
    async def settings(self, ctx):
        jail_role_id = await self.config.guild(ctx.guild).jail_role()
        if jail_role_id:
            jail_role = ctx.guild.get_role(jail_role_id)
            if not jail_role:
                await ctx.send("Jail role not found.")
                return
            await ctx.send(f"Jail role: {jail_role.name}")
        else:
            await ctx.send("Jail role is not configured for this guild.")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def jail(self, ctx, member: discord.Member):
        jail_role_id = await self.config.guild(ctx.guild).jail_role()
        if not jail_role_id:
            await ctx.send("Jail role is not configured for this guild.")
            return

        jail_role = ctx.guild.get_role(jail_role_id)
        if not jail_role:
            await ctx.send("Jail role not found.")
            return

        self.original_roles[member.id] = member.roles[1:]  # Exclude @everyone role
        await member.remove_roles(*self.original_roles[member.id])
        await member.add_roles(jail_role)
        await ctx.send(f"{member.display_name} has been jailed.")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unjail(self, ctx, member: discord.Member):
        jail_role_id = await self.config.guild(ctx.guild).jail_role()
        if not jail_role_id:
            await ctx.send("Jail role is not configured for this guild.")
            return

        jail_role = ctx.guild.get_role(jail_role_id)
        if not jail_role:
            await ctx.send("Jail role not found.")
            return

        if member.id in self.original_roles:
            await member.remove_roles(jail_role)
            await member.add_roles(*self.original_roles[member.id], atomic=True)
            del self.original_roles[member.id]
            await ctx.send(f"{member.display_name} has been unjailed.")
        else:
            await ctx.send(f"{member.display_name} is not currently jailed.")


def setup(bot):
    bot.add_cog(WardenCog(bot))
    