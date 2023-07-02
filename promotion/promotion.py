import discord
from redbot.core import commands, Config, utils, checks, bot

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

    @promotion.command()
    @commands.admin()
    async def set_promotion_channel(self, ctx, channel: discord.TextChannel = None):
        guild_id = ctx.guild.id

        if channel is None:
            self.guild_settings[guild_id] = None
            await ctx.send("The promotion notification channel has been unset.")
        else:
            self.guild_settings[guild_id] = channel.id
            await ctx.send(f"The promotion notification channel has been set to {channel.mention}.")

    @promotion.command()
    @commands.admin()
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
    @commands.admin()
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

    @promotion.command()
    @commands.admin()
    async def promote(self, ctx, user: discord.Member, role: discord.Role):
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
                            blocks = ""
                            for c in after.display_name:
                                if c.isalpha():
                                    blocks += ":regional_indicator_{}: ".format(c).lower()
                                elif c.isdigit():
                                    blocks += self.numbers[int(c)]
                                else:
                                    blocks += " "
                            await promotion_channel.send(f"Congratulations to {after.mention} for being promoted to {blocks}!")

def setup(bot):
    bot.add_cog(Promotion(bot))

