import redbot.core.commands as commands

class WompCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        content = message.content.lower()
        if "womp" in content:
            await message.channel.send("womp")

bot.add_cog(WompCog(bot))
