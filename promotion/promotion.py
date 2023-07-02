import discord
from redbot.core import commands, Config, utils, checks, bot

class Promotion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890, force_registration=True)
        default_guild_settings = {
            "staff_roles": [],  # List of role IDs to monitor for promotions
            "notification_channel": "general"  # Replace with the desired channel name
        }
        self.config.register_guild(**default_guild_settings)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        guild = after.guild
        staff_roles = await self.config.guild(guild).staff_roles()
        notification_channel = await self.config.guild(guild).notification_channel()

        new_roles = [role.id for role in after.roles if role.id not in [role.id for role in before.roles]]
        promoted_roles = list(set(new_roles).intersection(staff_roles))

        if promoted_roles:
            role_names = [guild.get_role(role_id).name for role_id in promoted_roles]
            mention = after.mention
            message = f"{mention} has been promoted to {', '.join(role_names)}!"
            channel = guild.get_channel(notification_channel)
            await channel.send(message)

def setup(bot):
    bot.add_cog(Promotion(bot))

