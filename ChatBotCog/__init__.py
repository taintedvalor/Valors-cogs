from .main import ChatBotCog


async def setup(bot):
    await bot.add_cog(ChatBotCog(bot))
