from .Pinterest import PinterestCog


async def setup(bot):
    await bot.add_cog(PinterestCog(bot))
