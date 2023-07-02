from .promotion import PromotionCog


async def setup(bot):
    await bot.add_cog(PromotionCog(bot))
