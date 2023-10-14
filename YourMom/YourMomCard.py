import discord
from redbot.core import commands
import random

class YourMomCard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        content = message.content.lower()
        
        # Check if the message author is the RedBot instance
        if message.author.id == self.bot.user.id:
            return

        if any(trigger in content for trigger in ['hi mom', 'your mom', 'mum', 'hello mom']):
            response = self.get_random_response(message.author.display_name)
            await message.channel.send(response)

    def get_random_response(self, user_name):
        responses = [
            f"Hi {user_name}'s mom! 🌟",
            f"mom says hi",
            f"Is that you, mom? I have been looking for you! 👀",
            f"Hi {user_name}! Your mom told me to tell you to clean your room. 🧹",
            f"{user_name}, your mom called. idk why tho 🥦",
            # Additional responses
            f"hi um {user_name}, your mom and I were just playing",
            f"{user_name}, your mom and I just finished redecorating the living room. It's fabulous! 💐🖼️",
            f"Guess what, {user_name}? Your mom and I are having a movie night you will have the house to yourself be good!",
            f"{user_name}, your mom and I are cooking dinner together. She's teaching me her secret recipes! 🍝👩‍🍳",
        ]
        return random.choice(responses)

def setup(bot):
    bot.add_cog(YourMomCard(bot))
