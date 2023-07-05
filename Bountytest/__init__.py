from .BountyBoard import BountyBoard


async def setup(bot):
    await bot.add_cog(BountyBoard(bot))
