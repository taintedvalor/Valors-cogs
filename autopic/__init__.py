from .autopic import autopic


async def setup(bot):
    await bot.add_cog(autopic(bot))
