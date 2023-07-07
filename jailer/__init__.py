from .jailer import Jail


async def setup(bot):
    await bot.add_cog(Jail(bot))
