import asyncio

from redbot.core.bot import Red

from .randimages import RandImages

from .roleplaycog import RolePlayCog

__red_end_user_data_statement__ = (
    "This cog does not persistently store data about users."
)


async def setup(bot: Red) -> None:
    cog = RolePlayCog(bot)

    if asyncio.iscoroutinefunction(bot.add_cog):
        await bot.add_cog(cog)
    else:
        bot.add_cog(cog)


async def setup(bot: Red):
    cog = RandImages(bot)
    await bot.add_cog(cog)
