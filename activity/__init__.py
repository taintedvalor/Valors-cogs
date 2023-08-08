from .Activity import Activity


async def setup(bot):
    await bot.add_cog(Activity(bot))
