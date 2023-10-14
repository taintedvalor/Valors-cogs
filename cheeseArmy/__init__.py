from .CheeseArmy import CheeseArmy


async def setup(bot):
    await bot.add_cog(CheeseArmy(bot))
