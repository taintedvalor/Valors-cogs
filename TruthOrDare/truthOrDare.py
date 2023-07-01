import asyncio
import functools
from typing import List, Optional, Union

import discord
from discord import ButtonStyle, Interaction
from discord.ui import Button, View
from redbot.core import commands
from random import choice
from discord.ext import commands
from discord.ui import Button, View
import random

class TruthOrDareCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def truth_or_dare(self, ctx):
        truths = [
            "What is your biggest fear?",
            "What is your most embarrassing moment?",
            "Have you ever cheated on a test?",
            "What is the craziest thing you've done?",
            "What is your secret talent?",
            "Have you ever lied to your best friend?",
            # Add more truth questions here
        ]

        dares = [
            "Sing a song in a funny voice.",
            "Do a cartwheel or a somersault.",
            "Prank call a friend.",
            "Dance like nobody's watching.",
            "Eat a spoonful of a condiment of your choice.",
            "Do 10 push-ups right now.",
            # Add more dare tasks here
        ]

        nsfw_options = [
            "Describe your wildest fantasy.",
            "What is your most intimate secret?",
            "Have you ever had a one-night stand?",
            "What is your favorite position?",
            "Share your most embarrassing intimate moment.",
            "Have you ever used a dating app?",
            # Add more NSFW options here
        ]

        def get_random_question():
            button = random.choice(["Truth", "Dare", "NSFW"])

            if button == "Truth":
                return random.choice(truths)
            elif button == "Dare":
                return random.choice(dares)
            elif button == "NSFW":
                return random.choice(nsfw_options)
            else:
                return "Oops! Something went wrong."

        view = View()
        view.add_item(Button(label="Truth", style=ButtonStyle.primary, custom_id="truth"))
        view.add_item(Button(label="Dare", style=ButtonStyle.primary, custom_id="dare"))
        view.add_item(Button(label="NSFW", style=ButtonStyle.danger, custom_id="nsfw"))

        message = await ctx.send("Click a button to get a question or task!", view=view)

        def check(interaction):
            return interaction.message.id == message.id and interaction.user.id == ctx.author.id

        try:
            interaction = await self.bot.wait_for("button_click", check=check, timeout=60)
        except asyncio.TimeoutError:
            await message.edit(content="You took too long to respond!")
            await message.clear_reactions()
            return

        await interaction.response.defer()

        if interaction.custom_id == "truth":
            response = random.choice(truths)
        elif interaction.custom_id == "dare":
            response = random.choice(dares)
        elif interaction.custom_id == "nsfw":
            response = random.choice(nsfw_options)
        else:
            response = "Oops! Something went wrong."

        await message.edit(content=f"{interaction.user.mention} {response}")
        await message.clear_reactions()

def setup(bot):
    bot.add_cog(TruthOrDareCog(bot))
