import discord
from redbot.core import commands
import random

class TruthOrDare(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def random_message(self, ctx):
        messages = [
            "Hello!",
            "How are you today?",
            "Nice to meet you!",
            "What's your favorite color?",
            "Have a great day!",
        ]
        random_message = random.choice(messages)
        message = await ctx.send(f"Click the reaction to get a random message: {random_message}")
        await message.add_reaction("🎲")

        def reaction_check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == "🎲"

        try:
            reaction, _ = await self.bot.wait_for(
                "reaction_add", check=reaction_check, timeout=30.0
            )
        except asyncio.TimeoutError:
            await ctx.send("You didn't click the reaction in time.")
        else:
            await ctx.send(f"Your random message: {random_message}")

def setup(bot):
    bot.add_cog(TruthOrDare(bot))
