from .jail import Redbox


async def setup(bot):
    await bot.add_cog(Redbox(bot))
