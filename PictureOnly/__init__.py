from .PictureOnly import PictureOnly


async def setup(bot):
    await bot.add_cog(PictureOnly(bot))
