from .jail import Jail


async def setup(bot):
    await bot.add_cog(Jail(bot))
