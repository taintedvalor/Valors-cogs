from .venting import Venting

async def setup(bot):
    cog = Venting(bot)
    await cog.initialize()
    bot.add_cog(cog)
