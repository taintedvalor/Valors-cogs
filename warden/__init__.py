from .warden import ward


async def setup(bot):
    await bot.add_cog(ward(bot))
