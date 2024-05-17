from .Valor import Valor


async def setup(bot):
    await bot.add_cog(Valor(bot))
