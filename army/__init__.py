from .Army import Army


async def setup(bot):
    await bot.add_cog(Army(bot))
