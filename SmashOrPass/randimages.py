import re
import random
from redbot.core import commands
from redbot.core.bot import Red

class WompCog(commands.Cog):
    def __init__(self, bot: Red):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        content = message.content.lower()
        matches = re.findall(r'\b(w+[o]+m+p+)\b', content)
        
        if matches:
            for match in matches:
                count = len(match)
                if count > 3:
                    varied_count = random.randint(3, count)
                    response = match * varied_count
                else:
                    response = match * count
                
                await message.channel.send(response)

def setup(bot: Red):
    bot.add_cog(WompCog(bot))
