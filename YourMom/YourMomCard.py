import discord
from redbot.core import commands
import random

class YourMomCard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        content = message.content.lower()
        if 'hi mom' in content:
            response = self.get_random_response(message.author.display_name)
            await message.channel.send(response)

    def get_random_response(self, user_name):
        responses = [
            f"Hi {user_name}'s mom! 🌟",
            f"{user_name}, your mom says hi 👋",
            f"Is that you, {user_name}? mom i was looking for you! 👀",
            f"Hi {user_name}! Your mom told me to tell you to clean your room. 🧹",
            f"{user_name}, your mom called. idk why tho"
            # Add more funny responses as needed
        ]
        return random.choice(responses)

def setup(bot):
    bot.add_cog(YourMomCard(bot))
