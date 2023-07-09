from .Offend import Offend


async def setup(bot):
    await bot.add_cog(Offend(bot))
