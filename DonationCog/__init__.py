from .DonationCog import DonationCog


async def setup(bot):
    await bot.add_cog(DonationCog(bot))
