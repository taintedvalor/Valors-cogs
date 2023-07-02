import discord
from redbot.core import commands, checks, bot

BaseCog = getattr(commands, "Cog", object)

class PromotionNotifierCog(commands.Cog):
    def __init__(self, bot_instance: bot):
        self.bot = bot_instance

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        guild = before.guild
        promotion_roles = await self.bot.get_cog_data(guild, "promotion_roles")
        if promotion_roles:
            added_roles = [role for role in after.roles if role.id in promotion_roles and role not in before.roles]
            if added_roles:
                await self.send_promotion_notification(guild, after, added_roles)

    async def send_promotion_notification(self, guild: discord.Guild, member: discord.Member, roles: list):
        promotion_channel_id = await self.bot.get_cog_data(guild, "promotion_channel")
        if promotion_channel_id:
            promotion_channel = guild.get_channel(promotion_channel_id)
            if promotion_channel:
                role_names = ", ".join(role.name for role in roles)
                message = f"🎉 {member.mention} has been promoted to {role_names}! 🎉"
                await promotion_channel.send(message)

    @commands.command(pass_context=True, rest_is_raw=True)
    @checks.admin_or_permissions(manage_guild=True)
    async def set_promotion_roles(self, ctx, *roles: discord.Role):
        """Set the roles that trigger promotion notifications."""
        guild = ctx.guild
        promotion_roles = [role.id for role in roles]
        await self.bot.set_cog_data(guild, "promotion_roles", promotion_roles)
        role_names = ", ".join(role.name for role in roles)
        await ctx.send(f"The promotion roles have been set to: {role_names}.")

    @commands.command(pass_context=True, rest_is_raw=True)
    @checks.admin_or_permissions(manage_guild=True)
    async def set_promotion_channel(self, ctx, channel: discord.TextChannel):
        """Set the channel to send promotion notifications."""
        guild = ctx.guild
        await self.bot.set_cog_data(guild, "promotion_channel", channel.id)
        await ctx.send(f"The promotion notification channel has been set to {channel.mention}.")

def setup(bot):
    bot.add_cog(PromotionNotifierCog(bot))
