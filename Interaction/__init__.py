import asyncio
from redbot.core.bot import Red
from .randimages import RandImages
from .randimages import NekosBest

__red_end_user_data_statement__ = (
    "This cog does not persistently store data or metadata about users."
)


async def setup(bot: Red):
    cog = RandImages(bot)
    await bot.add_cog(cog)


async def setup(bot: Red) -> None:
    cog = NekosBest(bot)
    await bot.add_cog(cog)
