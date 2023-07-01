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
        nsfw_button = Button(style=ButtonStyle.primary, label="NSFW", emoji="🔞")

        buttons_row = View()
        buttons_row.add_item(truth_button)
        buttons_row.add_item(dare_button)
        buttons_row.add_item(nsfw_button)

        await ctx.send("Choose your option:", view=buttons_row)

        def check(interaction):
            return interaction.user == ctx.author and interaction.message.id == ctx.message.id

        try:
            interaction = await self.bot.wait_for("button_click", check=check, timeout=30.0)
            await interaction.defer()

            if interaction.component.label == "Truth":
                await self.truth(ctx, nsfw=False)
            elif interaction.component.label == "Dare":
                await self.dare(ctx, nsfw=False)
            elif interaction.component.label == "NSFW":
                await self.nsfw_options(ctx)

        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond.")

    async def nsfw_options(self, ctx):
        truth_button = Button(style=ButtonStyle.primary, label="Truth (NSFW)", emoji="🔍")
        dare_button = Button(style=ButtonStyle.primary, label="Dare (NSFW)", emoji="🎯")
        back_button = Button(style=ButtonStyle.secondary, label="Back", emoji="↩️")

        buttons_row = View()
        buttons_row.add_item(truth_button)
        buttons_row.add_item(dare_button)
        buttons_row.add_item(back_button)

        await ctx.send("Choose NSFW option:", view=buttons_row)

        def check(interaction):
            return interaction.user == ctx.author and interaction.message.id == ctx.message.id

        try:
            interaction = await self.bot.wait_for("button_click", check=check, timeout=30.0)
            await interaction.defer()

            if interaction.component.label == "Truth (NSFW)":
                await self.truth(ctx, nsfw=True)
            elif interaction.component.label == "Dare (NSFW)":
                await self.dare(ctx, nsfw=True)
            elif interaction.component.label == "Back":
                await self.tod(ctx)

        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond.")

    async def truth(self, ctx, nsfw: bool = False):
        """Get a random truth"""
        if nsfw:
            truth_questions = [
                # NSFW truth questions
                "What is your wildest sexual fantasy?",
                "Have you ever had a one-night stand?",
                "What is your favorite position?",
                # Add more NSFW truth questions here
            ]
        else:
            truth_questions = [
                # Non-NSFW truth questions
                "What is your biggest fear?",
                "Have you ever cheated on a test?",
                "What is the most embarrassing thing you've done?",
                # Add more non-NSFW truth questions here
            ]
        question = choice(truth_questions)

        await ctx.send(f"**Truth:** {question}")

    async def dare(self, ctx, nsfw: bool = False):
        """Get a random dare"""
        if nsfw:
            dares = [
                # NSFW dares
                "Masturbate in a voice channel",
                "Give someone a lap dance",
                "Roleplay a steamy scene with a friend",
                # Add more NSFW dares here
            ]
        else:
            dares = [
                # Non-NSFW dares
                "Sing a song in a public voice channel",
                "Do 10 push-ups right now",
                "Tell a joke that will make everyone laugh",
                # Add more non-NSFW dares here
            ]
        dare = choice(dares)

        await ctx.send(f"**Dare:** {dare}")

def setup(bot):
    bot.add_cog(TruthOrDare(bot))
