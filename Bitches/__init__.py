from .Bitches import Bitches


async def setup(bot):
    await bot.add_cog(Bitches(bot))
