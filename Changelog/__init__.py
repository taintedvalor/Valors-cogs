from .ChangelogCog import ChangelogCog


async def setup(bot):
    await bot.add_cog(ChangelogCog(bot))
