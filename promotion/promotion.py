import discord
from redbot.core import commands, Config

class Promotion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)
        default_guild_settings = {
            "promotion_channel": None,
            "staff_roles": []
        }
        self.config.register_guild(**default_guild_settings)
        self.numbers = [':zero:', ':one:', ':two:', ':three:',
                        ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:']

    async def guild_settings(self, guild):
        return await self.config.guild(guild).all()

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
        settings = await self.guild_settings(ctx.guild)

        if channel is None:
            settings["promotion_channel"] = None
            await ctx.send("The promotion notification channel has been unset.")
        else:
            settings["promotion_channel"] = channel.id
            await ctx.send(f"The promotion notification channel has been set to {channel.mention}.")

    @promotion.command(name="addrole")
    @commands.admin()
    async def add_staff_role(self, ctx, role: discord.Role, rank: int = 1):
        """
        Adds a staff role for promotions.

        Usage: !promotion addrole [role] [rank]
        """
        settings = await self.guild_settings(ctx.guild)
        staff_roles = settings["staff_roles"]

        if any(staff_role["role"].id == role.id for staff_role in staff_roles):
            await ctx.send(f"The {role.name} role is already added as a staff role.")
            return

        staff_roles.append({"role": role, "rank": rank})
        staff_roles.sort(key=lambda r: r["rank"])
        settings["staff_roles"] = staff_roles
        await ctx.send(f"The {role.name} role has been added as a staff role with rank {rank}.")

    @promotion.command(name="removerole")
    @commands.admin()
    async def remove_staff_role(self, ctx, role: discord.Role):
        """
        Removes a staff role from promotions.

        Usage: !promotion removerole [role]
        """
        settings = await self.guild_settings(ctx.guild)
        staff_roles = settings["staff_roles"]

        if any(staff_role["role"].id == role.id for staff_role in staff_roles):
            staff_roles = [staff_role for staff_role in staff_roles if staff_role["role"].id != role.id]
            settings["staff_roles"] = staff_roles
            await ctx.send(f"The {role.name} role has been removed from the staff roles.")
        else:
            await ctx.send(f"The {role.name} role is not currently a staff role.")

    @promotion.command()
    @commands.admin()
    async def promote(self, ctx, user: discord.Member, rank: int = None):
        """
        Promotes a user to a specified role based on rank number.

        Usage: !promotion promote [user] [rank]
        """
        settings = await self.guild_settings(ctx.guild)
        staff_roles = settings["staff_roles"]

        if not staff_roles:
            await ctx.send("No staff roles have been configured for this guild.")
            return

        current_roles = [staff_role["role"] for staff_role in staff_roles if staff_role["role"] in user.roles]

        if rank is None:
            if current_roles:
                current_rank = max(staff_roles.index(staff_role) for staff_role in staff_roles if staff_role["role"] in current_roles)
                if current_rank + 1 < len(staff_roles):
                    role = staff_roles[current_rank + 1]["role"]
                else:
                    role = staff_roles[current_rank]["role"]
            else:
                role = staff_roles[0]["role"]
        else:
            if rank < 1 or rank > len(staff_roles):
                await ctx.send("Invalid rank number.")
                return
            else:
                role = staff_roles[rank - 1]["role"]

        if role in [staff_role["role"] for staff_role in staff_roles]:
            if role in current_roles:
                await ctx.send(f"{user.name} already has the {role.name} role.")
            else:
                await user.add_roles(role)
                promotion_channel_id = settings["promotion_channel"]

                if promotion_channel_id:
                    promotion_channel = ctx.guild.get_channel(promotion_channel_id)
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
                await ctx.send(f"{user.name} has been promoted to the {role.name} role.")
        else:
            await ctx.send(f"{role.name} is not a staff role.")

    @promotion.command()
    @commands.admin()
    async def demote(self, ctx, user: discord.Member):
        """
        Demotes a user by removing all staff roles.

        Usage: !promotion demote [user]
        """
        settings = await self.guild_settings(ctx.guild)
        staff_roles = settings["staff_roles"]

        if not staff_roles:
            await ctx.send("No staff roles have been configured for this guild.")
            return

        current_roles = [staff_role["role"] for staff_role in staff_roles if staff_role["role"] in user.roles]

        if current_roles:
            await user.remove_roles(*current_roles)
            await ctx.send(f"All staff roles have been removed from {user.name}.")
        else:
            await ctx.send(f"{user.name} does not have any staff roles.")

    @promotion.command(name="list")
    @commands.admin()
    async def list_settings(self, ctx):
        """
        Lists the promotion settings for the guild.

        Usage: !promotion list
        """
        settings = await self.guild_settings(ctx.guild)
        promotion_channel_id = settings["promotion_channel"]
        staff_roles = settings["staff_roles"]

        response = f"Promotion Settings:\n"
        response += f"Promotion Channel: {ctx.guild.get_channel(promotion_channel_id).mention}\n" if promotion_channel_id else "Promotion Channel: None\n"
        response += "Staff Roles:\n"
        if staff_roles:
            for index, staff_role in enumerate(staff_roles, start=1):
                role = staff_role["role"]
                rank = staff_role["rank"]
                response += f"{index}. {role.name} (Rank: {rank})\n"
        else:
            response += "No staff roles have been added.\n"

        await ctx.send(response)

def setup(bot):
    bot.add_cog(Promotion(bot))
