from .ElectionCog import Election


async def setup(bot):
    await bot.add_cog(Election(bot))
