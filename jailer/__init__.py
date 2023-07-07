from .jailer import jail


async def setup(bot):
    await bot.add_cog(jail(bot))
