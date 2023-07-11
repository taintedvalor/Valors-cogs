from .warden import WardenCog


async def setup(bot):
    await bot.add_cog(WardenCog(bot))
