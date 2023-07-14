from .Pinterest import PinterestScraper


async def setup(bot):
    await bot.add_cog(PinterestScraper(bot))
