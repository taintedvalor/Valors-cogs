from .VoiceActivity import VoiceActivity


async def setup(bot):
    await bot.add_cog(VoiceActivity(bot))
