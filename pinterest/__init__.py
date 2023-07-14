from .Pinterest import ImageScraperCog


async def setup(bot):
    await bot.add_cog(ImageScraperCog(bot))
