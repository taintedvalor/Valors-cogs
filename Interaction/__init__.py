from .Interaction import InteractionsCog


async def setup(bot):
    await bot.add_cog(InteractionsCog(bot))
