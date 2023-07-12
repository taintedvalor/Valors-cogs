from .jailer import Jailer


async def setup(bot):
    await bot.add_cog(Jailer(bot))
