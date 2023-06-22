from .venting_cog import VentCog


async def setup(bot):
    await bot.add_cog(VentCog(bot))
