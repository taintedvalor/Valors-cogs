from .InfiniteSentence import InfiniteSentence


async def setup(bot):
    await bot.add_cog(InfiniteSentence(bot))
