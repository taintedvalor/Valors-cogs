from .ElectionCog import ElectionCog


async def setup(bot):
    await bot.add_cog(ElectionCog(bot))
