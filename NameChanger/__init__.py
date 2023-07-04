from .NameChanger import NameChanger


async def setup(bot):
    await bot.add_cog(NameChanger(bot))
