from redbot.core.bot import Red
from .randimages import SmashOrPass

__red_end_user_data_statement__ = (
    "This cog does not persistently store data or metadata about users."
)


async def setup(bot: Red):
    cog = SmashOrPass(bot)
    await bot.add_cog(cog)
