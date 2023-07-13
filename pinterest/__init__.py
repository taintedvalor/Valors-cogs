from .Pinterest import Pinterest


async def setup(bot):
    await bot.add_cog(Pinterest(bot))
