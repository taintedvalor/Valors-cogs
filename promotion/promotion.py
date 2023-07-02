import discord
from redbot.core import commands, Config, utils, checks, bot

class PromotionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild_settings = {}  # Dictionary to store guild settings

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def promotion(self, ctx):
        """Main promotion command."""
        pass

    @promotion.command()
    @commands.has_permissions(administrator=True)
    async def set_promotion_channel(self, ctx, channel: discord.TextChannel = None):
        guild_id = ctx.guild.id

        if channel is None:
            self.guild_settings[guild_id] = None
            await ctx.send("The promotion notification channel has been unset.")
        else:
            self.guild_settings[guild_id] = channel.id
            await ctx.send(f"The promotion notification channel has been set to {channel.mention}.")

    @promotion.command()
    @commands.has_permissions(administrator=True)
    async def add_staff_role(self, ctx, role: discord.Role):
        guild_id = ctx.guild.id

        if guild_id not in self.guild_settings:
            self.guild_settings[guild_id] = {"staff_roles": [role.id]}
        else:
            if "staff_roles" not in self.guild_settings[guild_id]:
                self.guild_settings[guild_id]["staff_roles"] = [role.id]
            elif role.id not in self.guild_settings[guild_id]["staff_roles"]:
                self.guild_settings[guild_id]["staff_roles"].append(role.id)

        await ctx.send(f"The {role.name} role has been added as a staff role.")

    @promotion.command()
    @commands.has_permissions(administrator=True)
    async def remove_staff_role(self, ctx, role: discord.Role):
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

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        guild_id = after.guild.id
        if guild_id in self.guild_settings:
            promotion_channel_id = self.guild_settings[guild_id]

            if promotion_channel_id is not None:
                promotion_channel = after.guild.get_channel(promotion_channel_id)
                if promotion_channel is not None:
                    staff_role_ids = [role.id for role in after.roles]
                    for staff_role_id in self.guild_settings[guild_id]["staff_roles"]:
                        if staff_role_id in staff_role_ids and staff_role_id not in [role.id for role in before.roles]:
                            await promotion_channel.send(f"Congratulations to {after.mention} for being promoted to a staff member!")

def setup(bot):
    bot.add_cog(PromotionCog(bot))


