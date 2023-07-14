from .Pinterest import ImageScrapingCog


async def setup(bot):
    await bot.add_cog(ImageScrapingCog(bot))
