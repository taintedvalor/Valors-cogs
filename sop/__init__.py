from .sop import SmashOrPass


async def setup(bot):
    await bot.add_cog(SmashOrPass(bot))
