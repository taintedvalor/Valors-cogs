from .Womp import Womp


async def setup(bot):
    await bot.add_cog(Womp(bot))
