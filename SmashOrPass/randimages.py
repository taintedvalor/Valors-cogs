from redbot.core import commands

class WompCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        if "womp womp" in message.content.lower():
            await message.channel.send("womp womp")

def setup(bot):
    bot.add_cog(WompCog(bot))
