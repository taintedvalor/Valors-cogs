import asyncio
from discord import Embed, Message
from redbot.core import commands, Config, checks

class Jail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def jail(self, ctx, user: discord.Member):
        jail_role = discord.utils.get(ctx.guild.roles, name="Jail")
        if not jail_role:
            # Create the jail role if it doesn't exist
            jail_role = await ctx.guild.create_role(name="Jail")

            # Set the permissions for the jail role
            for channel in ctx.guild.channels:
                # Disable all permissions for the jail role
                await channel.set_permissions(jail_role, send_messages=False, read_messages=True)

        # Save the user's current roles
        user_roles = user.roles[1:]

        # Remove all roles from the user
        await user.remove_roles(*user.roles[1:])
        await user.add_roles(jail_role)

        # Create a jail channel
        jail_channel = await ctx.guild.create_text_channel(name=f"jail-{user.display_name}")
        await jail_channel.set_permissions(jail_role, send_messages=True, read_messages=True)

        # Send a message indicating that the user has been jailed
        await ctx.send(f"{user.mention} has been jailed.")

        # Store the user's original roles and jail channel in custom attributes of the user object
        setattr(user, "original_roles", user_roles)
        setattr(user, "jail_channel", jail_channel)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unjail(self, ctx, user: discord.Member):
        jail_role = discord.utils.get(ctx.guild.roles, name="Jail")
        if not jail_role:
            await ctx.send("There is no jail role set up.")
            return

        # Retrieve the user's original roles and jail channel from the custom attributes
        user_roles = getattr(user, "original_roles", [])
        jail_channel = getattr(user, "jail_channel", None)

        # Restore the user's original roles
        await user.remove_roles(jail_role)
        await user.add_roles(*user_roles)

        # Delete the jail channel
        if jail_channel:
            await jail_channel.delete()

        # Send a message indicating that the user has been unjailed
        await ctx.send(f"{user.mention} has been unjailed.")

def setup(bot):
    bot.add_cog(Jail(bot))

