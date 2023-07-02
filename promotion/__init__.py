from .promotion import PromotionNotifierCog


async def setup(bot):
    await bot.add_cog(PromotionNotifierCog(bot))
