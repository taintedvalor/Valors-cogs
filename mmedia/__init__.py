from .MMedia import MMedia


async def setup(bot):
    await bot.add_cog(MMedia(bot))
