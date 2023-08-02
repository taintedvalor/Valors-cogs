from .MMedia import mmedia


async def setup(bot):
    await bot.add_cog(mmedia(bot))
