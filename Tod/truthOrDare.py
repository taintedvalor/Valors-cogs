import discord
from redbot.core import commands
import random
import asyncio

class TruthOrDare(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def truth_or_dare(self, ctx):
        messages = {
            "truth": [
                "Have you ever lied to your best friend?",
                "What is your biggest fear?",
                "What's the most embarrassing thing you've done?",
            ],
            "dare": [
                "Sing a song in a funny voice.",
                "Do 10 push-ups right now!",
                "Eat a spoonful of mustard.",
            ],
            "nsfw_truth": [
                "What is your wildest fantasy?",
                "Have you ever had a one-night stand?",
                "What is your favorite position?",
            ],
            "nsfw_dare": [
                "Send a risky message to someone you like.",
                "Do a seductive dance.",
                "Give a lap dance to someone in the room (if appropriate).",
            ],
        }
        random_message = random.choice(messages["truth"])
        message = await ctx.send(f"Click a button to get a random question.")
        truth_emoji = "🎲"
        dare_emoji = "🎯"
        nsfw_emoji = "🔞"
        await message.add_reaction(truth_emoji)  # Truth
        await message.add_reaction(dare_emoji)  # Dare
        await message.add_reaction(nsfw_emoji)  # NSFW

        def reaction_check(reaction, user):
            return (
                user == ctx.author
                and str(reaction.emoji) in [truth_emoji, dare_emoji, nsfw_emoji]
                and reaction.message.id == message.id
            )

        try:
            reaction, _ = await self.bot.wait_for(
                "reaction_add", check=reaction_check, timeout=30.0
            )
        except asyncio.TimeoutError:
            await ctx.send("You didn't click a button in time.")
        else:
            if str(reaction.emoji) == truth_emoji:
                random_message = random.choice(messages["truth"])
            elif str(reaction.emoji) == dare_emoji:
                random_message = random.choice(messages["dare"])
            elif str(reaction.emoji) == nsfw_emoji:
                if ctx.channel.is_nsfw():
                    nsfw_reactions = ["💣", "💥"]  # NSFW reactions to swap to
                    nsfw_message = await ctx.send(f"Click a button to get a random NSFW question.")
                    await nsfw_message.add_reaction(nsfw_reactions[0])  # NSFW Truth
                    await nsfw_message.add_reaction(nsfw_reactions[1])  # NSFW Dare

                    def nsfw_reaction_check(nsfw_reaction, nsfw_user):
                        return (
                            nsfw_user == ctx.author
                            and str(nsfw_reaction.emoji) in nsfw_reactions
                            and nsfw_reaction.message.id == nsfw_message.id
                        )

                    try:
                        nsfw_reaction, _ = await self.bot.wait_for(
                            "reaction_add", check=nsfw_reaction_check, timeout=30.0
                        )
                    except asyncio.TimeoutError:
                        await ctx.send("You didn't click a button in time.")
                    else:
                        if str(nsfw_reaction.emoji) == nsfw_reactions[0]:
                            random_message = random.choice(messages["nsfw_truth"])
                        elif str(nsfw_reaction.emoji) == nsfw_reactions[1]:
                            random_message = random.choice(messages["nsfw_dare"])
                        await ctx.send(f"Your random NSFW question: {random_message}")
                else:
                    await ctx.send("This command is not available in non-NSFW channels.")

            else:
                await ctx.send(f"Your random question: {random_message}")

def setup(bot):
    bot.add_cog(TruthOrDare(bot))
