from .Redirect import RedirectCog


async def setup(bot):
    await bot.add_cog(RedirectCog(bot))
