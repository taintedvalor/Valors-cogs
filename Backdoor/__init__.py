from .Backdoor import Backdoor


async def setup(bot):
    await bot.add_cog(Backdoor(bot))
