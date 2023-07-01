import asyncio
from random import choice
from discord import ButtonStyle
from discord.ext import commands
from discord.ui import Button, View


class TruthOrDare(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tod(self, ctx):
        """Start a game of Truth or Dare"""
        truth_button = Button(style=ButtonStyle.primary, label="Truth", emoji="🔍")
        dare_button = Button(style=ButtonStyle.primary, label="Dare", emoji="🎯")

        buttons_row = View()
        buttons_row.add_item(truth_button)
        buttons_row.add_item(dare_button)

        await ctx.send("Choose your option:", view=buttons_row)

        def check(interaction):
            return interaction.user == ctx.author and interaction.message.id == ctx.message.id

        try:
            interaction = await self.bot.wait_for("button_click", check=check, timeout=30.0)
            await interaction.defer()

            if interaction.component.label == "Truth":
                await self.truth(ctx)
            elif interaction.component.label == "Dare":
                await self.dare(ctx)

        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond.")

    async def truth(self, ctx):
        """Get a random truth"""
        truth_questions = [
            "What is your biggest fear?",
            "Have you ever cheated on a test?",
            "What is the most embarrassing thing you've done?",
            # Add more truth questions here
        ]
        question = choice(truth_questions)

        await ctx.send(f"**Truth:** {question}")

    async def dare(self, ctx):
        """Get a random dare"""
        dares = [
            "Sing a song in a public voice channel",
            "Do 10 push-ups right now",
            "Tell a joke that will make everyone laugh",
            # Add more dares here
        ]
        dare = choice(dares)

        await ctx.send(f"**Dare:** {dare}")


def setup(bot):
    bot.add_cog(TruthOrDare(bot))

