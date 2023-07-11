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

    # Rest of the code remains the same

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
