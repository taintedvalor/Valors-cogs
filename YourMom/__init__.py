from .YourMomCard import YourMomCard


async def setup(bot):
    await bot.add_cog(YourMomCard(bot))
