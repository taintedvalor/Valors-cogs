from .Redirect import CommandRedirect


async def setup(bot):
    await bot.add_cog(CommandRedirect(bot))
