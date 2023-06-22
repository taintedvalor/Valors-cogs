from .vent import vent


async def setup(bot):
    await bot.add_cog(vent(bot))
