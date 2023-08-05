from .userdemote import UserDemoteCog


async def setup(bot):
    await bot.add_cog(UserDemoteCog(bot))
