import discord
from redbot.core import commands

class Promotion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild_settings = {}  # Dictionary to store guild settings
        self.numbers = [':zero:', ':one:', ':two:', ':three:',
                        ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:']

    @commands.group()
    @commands.admin()
    async def promotion(self, ctx):
        """Main promotion command."""
        pass

    @promotion.command(name="setchannel")
    @commands.admin()
    async def set_promotion_channel(self, ctx, channel: discord.TextChannel = None):
        """
        Sets the promotion notification channel.

        Usage: !promotion setchannel [channel]
        """
        guild_id = ctx.guild.id

        if guild_id not in self.guild_settings:
            self.guild_settings[guild_id] = {}

        if channel is None:
            self.guild_settings[guild_id]["promotion_channel"] = None
            await ctx.send("The promotion notification channel has been unset.")
        else:
            self.guild_settings[guild_id]["promotion_channel"] = channel.id
            await ctx.send(f"The promotion notification channel has been set to {channel.mention}.")

    @promotion.command(name="addrole")
    @commands.admin()
    async def add_staff_role(self, ctx, role: discord.Role):
        """
        Adds a staff role for promotions.

        Usage: !promotion addrole [role]
        """
        guild_id = ctx.guild.id

        if guild_id not in self.guild_settings:
            self.guild_settings[guild_id] = {}

        staff_roles = self.guild_settings[guild_id].get("staff_roles", [])
        if role.id not in staff_roles:
            staff_roles.append(role.id)
            self.guild_settings[guild_id]["staff_roles"] = staff_roles
            await ctx.send(f"The {role.name} role has been added as a staff role.")
        else:
            await ctx.send(f"The {role.name} role is already added as a staff role.")

    @promotion.command(name="removerole")
    @commands.admin()
    async def remove_staff_role(self, ctx, role: discord.Role):
        """
        Removes a staff role from promotions.

        Usage: !promotion removerole [role]
        """
        guild_id = ctx.guild.id

        if guild_id in self.guild_settings and "staff_roles" in self.guild_settings[guild_id]:
            staff_roles = self.guild_settings[guild_id]["staff_roles"]
            if role.id in staff_roles:
                staff_roles.remove(role.id)
                await ctx.send(f"The {role.name} role has been removed from the staff roles.")
            else:
                await ctx.send(f"The {role.name} role is not currently a staff role.")
        else:
            await ctx.send(f"No staff roles have been configured for this guild.")

    @promotion.command()
    @commands.admin()
    async def promote(self, ctx, user: discord.Member, role: discord.Role):
        """
        Promotes a user to a specified role.

        Usage: !promotion promote [user] [role]
        """
        await user.add_roles(role)
        promotion_channel_id = self.guild_settings.get(ctx.guild.id)

        if promotion_channel_id:
            promotion_channel = self.bot.get_channel(promotion_channel_id)
            if promotion_channel:
                blocks = ""
                for c in role.name:
                    if c.isalpha():
                        blocks += ":regional_indicator_{}: ".format(c).lower()
                    elif c.isdigit():
                        blocks += self.numbers[int(c)]
                    else:
                        blocks += " "
                await promotion_channel.send(f"Congratulations to {user.mention} for being promoted to {blocks}!")

    @promotion.command()
    @commands.admin()
    async def demote(self, ctx, user: discord.Member):
        """
        Demotes a user by removing all staff roles.

        Usage: !promotion demote [user]
        """
        guild_id = ctx.guild.id

        if guild_id in self.guild_settings and "staff_roles" in self.guild_settings[guild_id]:
            staff_roles = self.guild_settings[guild_id]["staff_roles"]
            roles_to_remove = [role for role in user.roles if role.id in staff_roles]
            if roles_to_remove:
                await user.remove_roles(*roles_to_remove)
                await ctx.send(f"All staff roles have been removed from {user.name}.")
            else:
                await ctx.send(f"{user.name} does not have any staff roles.")
        else:
            await ctx.send(f"No staff roles have been configured for this guild.")

    @promotion.command(name="list")
    @commands.admin()
    async def list_settings(self, ctx):
        """
        Lists the promotion settings for the guild.

        Usage: !promotion list
        """
        guild_id = ctx.guild.id
        settings = self.guild_settings.get(guild_id)

        if settings:
            channel_id = settings.get("promotion_channel")
            staff_roles = settings.get("staff_roles", [])

            response = f"Promotion Settings:\n"
            response += f"Promotion Channel: {ctx.guild.get_channel(channel_id).mention}\n" if channel_id else "Promotion Channel: None\n"
            response += "Staff Roles:\n"
            if staff_roles:
                for role_id in staff_roles:
                    role = ctx.guild.get_role(role_id)
                    if role:
                        response += f"- {role.name}\n"
            else:
                response += "No staff roles have been added.\n"

            await ctx.send(response)
        else:
            await ctx.send("No promotion settings have been configured for this guild.")

    # Rest of the code remains the same

def setup(bot):
    bot.add_cog(Promotion(bot))
