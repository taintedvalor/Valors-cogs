import discord
from redbot.core import commands


class Promotion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild_settings = {}  # Dictionary to store guild settings
        self.numbers = [
            ":zero:",
            ":one:",
            ":two:",
            ":three:",
            ":four:",
            ":five:",
            ":six:",
            ":seven:",
            ":eight:",
            ":nine:",
        ]

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
            await ctx.send(
                f"The promotion notification channel has been set to {channel.mention}."
            )

    @promotion.command(name="addrole")
    @commands.admin()
    async def add_staff_role(self, ctx, role: discord.Role, rank: int = 1):
        """
        Adds a staff role for promotions.

        Usage: !promotion addrole [role] [rank]
        """
        guild_id = ctx.guild.id

        if guild_id not in self.guild_settings:
            self.guild_settings[guild_id] = {}

        staff_roles = self.guild_settings[guild_id].get("staff_roles", [])
        existing_role_ranks = {r["role"].id: r["rank"] for r in staff_roles}

        if role.id in existing_role_ranks:
            await ctx.send(f"The {role.name} role is already added as a staff role.")
            return

        staff_roles.append({"role": role, "rank": rank})
        staff_roles.sort(key=lambda r: r["rank"], reverse=True)
        self.guild_settings[guild_id]["staff_roles"] = staff_roles

        await ctx.send(
            f"The {role.name} role has been added as a staff role with rank {rank}."
        )

    @promotion.command(name="removerole")
    @commands.admin()
    async def remove_staff_role(self, ctx, role: discord.Role):
        """
        Removes a staff role from promotions.

        Usage: !promotion removerole [role]
        """
        guild_id = ctx.guild.id

        if (
            guild_id in self.guild_settings
            and "staff_roles" in self.guild_settings[guild_id]
        ):
            staff_roles = self.guild_settings[guild_id]["staff_roles"]
            staff_roles = [r for r in staff_roles if r["role"].id != role.id]
            self.guild_settings[guild_id]["staff_roles"] = staff_roles
            await ctx.send(
                f"The {role.name} role has been removed from the staff roles."
            )
        else:
            await ctx.send(f"The {role.name} role is not currently a staff role.")


@promotion.command()
@commands.admin()
async def promote(self, ctx, user: discord.Member, role: discord.Role = None):
    """
    Promotes a user to a specified role.

    Usage: !promotion promote [user] [role]
    """
    guild_id = ctx.guild.id

    if (
        guild_id in self.guild_settings
        and "staff_roles" in self.guild_settings[guild_id]
    ):
        staff_roles = self.guild_settings[guild_id]["staff_roles"]
        if not staff_roles:
            await ctx.send("No staff roles have been configured for this guild.")
            return

        current_roles = [
            r["role"]
            for r in staff_roles
            if r["role"]["id"] in [r.id for r in user.roles]
        ]

        if role is None:
            if current_roles:
                current_highest_rank = max(
                    current_roles,
                    key=lambda r: next(
                        (
                            x["rank"]
                            for x in staff_roles
                            if x["role"]["id"] == r["role"]["id"]
                        ),
                        0,
                    ),
                )
                next_rank_roles = [
                    r
                    for r in staff_roles
                    if next(
                        (
                            x["rank"]
                            for x in staff_roles
                            if x["role"]["id"] == r["role"]["id"]
                        ),
                        0,
                    )
                    > next(
                        (
                            x["rank"]
                            for x in staff_roles
                            if x["role"]["id"] == current_highest_rank["role"]["id"]
                        ),
                        0,
                    )
                ]
                if next_rank_roles:
                    role = min(next_rank_roles, key=lambda r: r["rank"])
                else:
                    role = min(staff_roles, key=lambda r: r["rank"])
            else:
                role = min(staff_roles, key=lambda r: r["rank"])

        if role["role"]["id"] in [r["role"]["id"] for r in staff_roles]:
            if role["role"] in current_roles:
                await ctx.send(f"{user.name} already has the {role['role'].name} role.")
            else:
                await user.add_roles(role["role"])
                promotion_channel_id = self.guild_settings.get(ctx.guild.id, {}).get(
                    "promotion_channel"
                )

                if promotion_channel_id:
                    promotion_channel = self.bot.get_channel(promotion_channel_id)
                    if promotion_channel:
                        blocks = ""
                        for c in role["role"].name:
                            if c.isalpha():
                                blocks += ":regional_indicator_{}: ".format(c).lower()
                            elif c.isdigit():
                                blocks += self.numbers[int(c)]
                            else:
                                blocks += " "
                        await promotion_channel.send(
                            f"Congratulations to {user.mention} for being promoted to {blocks}!"
                        )
                await ctx.send(
                    f"{user.name} has been promoted to the {role['role'].name} role."
                )
        else:
            await ctx.send(f"{role['role'].name} is not a staff role.")
    else:
        await ctx.send("No staff roles have been configured for this guild.")

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
            response += (
                f"Promotion Channel: {ctx.guild.get_channel(channel_id).mention}\n"
                if channel_id
                else "Promotion Channel: None\n"
            )
            response += "Staff Roles:\n"
            if staff_roles:
                for staff_role in staff_roles:
                    role = staff_role["role"]
                    rank = staff_role["rank"]
                    response += f"- {role.name} (Rank: {rank})\n"
            else:
                response += "No staff roles have been added.\n"

            await ctx.send(response)
        else:
            await ctx.send("No promotion settings have been configured for this guild.")

    # Rest of the code remains the same


def setup(bot):
    bot.add_cog(Promotion(bot))
