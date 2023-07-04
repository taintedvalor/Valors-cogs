from .BountyCog import BountyCog


async def setup(bot):
    await bot.add_cog(BountyCog(bot))
