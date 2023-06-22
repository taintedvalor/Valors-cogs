from redbot.core.bot import Red
from .Venting import Venting
from discord_slash import SlashCommand


async def setup(bot: Red):
    if not hasattr(bot, "slash"):
        SlashCommand(
            bot, sync_commands=True, override_type=True, sync_on_cog_reload=True
        )
    await bot.add_cog(Venting(bot))
