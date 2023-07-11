from redbot.core.bot import Red
from .randimages import RandImages

__red_end_user_data_statement__ = (
    "This cog does not persistently store data or metadata about users."
)


async def setup(bot: Red) -> None:
    cog = RandImages(bot)

    if asyncio.iscoroutinefunction(bot.add_cog):
        await bot.add_cog(cog)
    else:
        bot.add_cog(cog)
