from redbot.core import commands, Config
import discord


class Jailer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)  # Replace with a unique identifier
        self.config.register_guild(jail_role=None, jail_channel=None)
        self.original_roles = {}

    @commands.group()
    @commands.has_permissions(manage_roles=True)
    async def jailer(self, ctx):
        """Commands for jail management."""
        pass

    @jailer.command(name="configjailrole")
    async def config_jail_role(self, ctx, role: discord.Role):
        """Configures the jail role."""
        guild = ctx.guild
        jail_role_id = role.id
        jail_channel_id = await self.config.guild(guild).jail_channel()

        if not jail_channel_id:
            await ctx.send("Jail channel is not configured for this guild.")
            return

        jail_role = guild.get_role(jail_role_id)
        jail_channel = guild.get_channel(jail_channel_id)

        if not jail_role:
            await ctx.send("Jail role not found.")
            return

        if not jail_channel:
            await ctx.send("Jail channel not found.")
            return

        # Set permissions for jail role in jail channel
        await jail_channel.set_permissions(jail_role, read_messages=True, send_messages=True)
        await self.update_channel_permissions(guild, jail_role, jail_channel)

        # Remove all roles from users with the jail role
        for member in guild.members:
            if jail_role in member.roles:
                await member.remove_roles(jail_role)

        await ctx.send(f"Jail role configured as {role.name}.")

    @jailer.command(name="configjailchannel")
    async def config_jail_channel(self, ctx, channel: discord.TextChannel):
        """Configures the jail channel."""
        guild = ctx.guild
        jail_channel_id = channel.id
        jail_role_id = await self.config.guild(guild).jail_role()

        if not jail_role_id:
            await ctx.send("Jail role is not configured for this guild.")
            return

        jail_role = guild.get_role(jail_role_id)
        jail_channel = guild.get_channel(jail_channel_id)

        if not jail_role:
            await ctx.send("Jail role not found.")
            return

        if not jail_channel:
            await ctx.send("Jail channel not found.")
            return

        # Set permissions for jail role in jail channel
        await jail_channel.set_permissions(jail_role, read_messages=True, send_messages=True)
        await self.update_channel_permissions(guild, jail_role, jail_channel)
        await ctx.send(f"Jail channel configured as {channel.mention}.")

    @jailer.command(name="settings")
    async def jailer_settings(self, ctx):
        """Shows the jailer settings for the guild."""
        guild_config = self.config.guild(ctx.guild)
        jail_role_id = await guild_config.jail_role()
        jail_channel_id = await guild_config.jail_channel()

        if jail_role_id:
            jail_role = ctx.guild.get_role(jail_role_id)
            if not jail_role:
                await ctx.send("Jail role not found.")
                return
            await ctx.send(f"Jail role: {jail_role.name}")
        else:
            await ctx.send("Jail role is not configured for this guild.")

        if jail_channel_id:
            jail_channel = ctx.guild.get_channel(jail_channel_id)
            if not jail_channel:
                await ctx.send("Jail channel not found.")
                return
            await ctx.send(f"Jail channel: {jail_channel.mention}")
        else:
            await ctx.send("Jail channel is not configured for this guild.")

    @jailer.command(name="jail")
    async def jail_member(self, ctx, member: discord.Member):
        """Jails a member."""
        guild_config = self.config.guild(ctx.guild)
        jail_role_id = await guild_config.jail_role()
        jail_channel_id = await guild_config.jail_channel()

        if not jail_role_id:
            await ctx.send("Jail role is not configured for this guild.")
            return

        if not jail_channel_id:
            await ctx.send("Jail channel is not configured for this guild.")
            return

        jail_role = ctx.guild.get_role(jail_role_id)
        if not jail_role:
            await ctx.send("Jail role not found.")
            return

        jail_channel = ctx.guild.get_channel(jail_channel_id)
        if not jail_channel:
            await ctx.send("Jail channel not found.")
            return

        self.original_roles[member.id] = member.roles[1:]  # Exclude @everyone role
        await member.remove_roles(*self.original_roles[member.id])
        await member.add_roles(jail_role)
        await self.update_channel_permissions(ctx.guild, jail_role, jail_channel)
        await ctx.send(f"{member.display_name} has been jailed.")
        await jail_channel.send(f"{member.display_name} has been jailed.")
        await self.config.guild(ctx.guild).original_roles.set_raw(member.id, value=self.original_roles[member.id])

    @jailer.command(name="unjail")
    async def unjail_member(self, ctx, member: discord.Member):
        """Unjails a member."""
        guild_config = self.config.guild(ctx.guild)
        jail_role_id = await guild_config.jail_role()
        jail_channel_id = await guild_config.jail_channel()

        if not jail_role_id:
            await ctx.send("Jail role is not configured for this guild.")
            return

        if not jail_channel_id:
            await ctx.send("Jail channel is not configured for this guild.")
            return

        jail_role = ctx.guild.get_role(jail_role_id)
        if not jail_role:
            await ctx.send("Jail role not found.")
            return

        jail_channel = ctx.guild.get_channel(jail_channel_id)
        if not jail_channel:
            await ctx.send("Jail channel not found.")
            return

        if member.id in self.original_roles:
            await member.remove_roles(jail_role)
            await member.add_roles(*self.original_roles[member.id], atomic=True)
            del self.original_roles[member.id]
            await self.update_channel_permissions(ctx.guild, jail_role, jail_channel)
            await ctx.send(f"{member.display_name} has been unjailed.")
            await jail_channel.send(f"{member.display_name} has been unjailed.")
        else:
            await ctx.send(f"{member.display_name} is not currently jailed.")

    async def update_channel_permissions(self, guild, jail_role, jail_channel):
        """Updates the channel permissions for a jail role."""
        for channel in guild.channels:
            if channel != jail_channel:
                await channel.set_permissions(jail_role, read_messages=False, send_messages=False)
                await self.config.guild(ctx.guild).original_roles.set_raw(member.id, value=self.original_roles[member.id])

   
    async def cog_unload(self):
        # Save all the cog data to the database upon cog unload
        for guild in self.bot.guilds:
            await self.config.guild(guild).clear_raw("original_roles")

def setup(bot):
    bot.add_cog(Jailer(bot))







