from discord.ext import commands
from redbot.core import commands
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
import random

class TruthOrDare(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tod(self, ctx):
        """Start a game of Truth or Dare"""
        truth_button = {
            "style": 1,  # ButtonStyle.primary
            "label": "Truth",
            "emoji": "🔍"
        }
        dare_button = {
            "style": 1,  # ButtonStyle.primary
            "label": "Dare",
            "emoji": "🎯"
        }

        buttons = [truth_button, dare_button]

        await ctx.send("Choose your option:", components=buttons)

        def check(res):
            return res.user.id == ctx.author.id and res.channel.id == ctx.channel.id

        try:
            res = await self.bot.wait_for("button_click", check=check, timeout=30.0)
            await res.respond(type=6)  # Acknowledge the button click

            if res.component.label == "Truth":
                await self.truth(ctx)
            elif res.component.label == "Dare":
                await self.dare(ctx)

        except TimeoutError:
            await ctx.send("You took too long to respond.")

    async def truth(self, ctx):
        """Get a random truth"""
        truth_questions = [
            "What is your biggest fear?",
            "Have you ever cheated on a test?",
            "What is the most embarrassing thing you've done?",
            # Add more truth questions here
        ]
        question = random.choice(truth_questions)

        await ctx.send(f"**Truth:** {question}")

    async def dare(self, ctx):
        """Get a random dare"""
        dares = [
            "Sing a song in a public voice channel",
            "Do 10 push-ups right now",
            "Tell a joke that will make everyone laugh",
            # Add more dares here
        ]
        dare = random.choice(dares)

        await ctx.send(f"**Dare:** {dare}")


def setup(bot):
    bot.add_cog(TruthOrDare(bot))
