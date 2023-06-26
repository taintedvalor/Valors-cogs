import discord
from discord import Embed
from redbot.core import commands
from random import choice

class TruthOrDare(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def truth(self, ctx, nsfw: bool = False):
        """Get a random truth question"""
        if nsfw:
            truth_questions = [
                "What is your wildest sexual fantasy?",
                "Have you ever had a one-night stand?",
                "What is your favorite position?",
                "Have you ever engaged in BDSM?",
                "What is the kinkiest thing you've ever done?",
                "Have you ever watched or read adult content?",
                "What is your most embarrassing intimate moment?",
                "What is your secret fetish?",
                "Have you ever had a threesome?",
                "What is your favorite place to have intimate encounters?",
                "Have you ever been caught in a compromising situation?",
                "What is the most adventurous place you've had intimacy?",
                "Have you ever used adult toys?",
                "What is the naughtiest thing you've ever done?",
                "Have you ever had a friends-with-benefits arrangement?",
                "What is your favorite roleplay scenario?",
                "Have you ever had a same-sex experience?",
                "What is your opinion on open relationships?",
                "What is your most memorable romantic encounter?",
                "Have you ever had a crush on a friend's partner?",
                # Add more NSFW truth questions here
            ]
        else:
            truth_questions = [
                "What is your biggest fear?",
                "Have you ever cheated on a test?",
                "What is the most embarrassing thing you've done?",
                "What is your secret talent?",
                "What is your dream job?",
                "Have you ever lied to your best friend?",
                "What is your guilty pleasure?",
                "What is your most embarrassing nickname?",
                "Have you ever had a crush on a teacher?",
                "What is the most adventurous thing you've done?",
                "Have you ever stolen anything?",
                "What is the strangest dream you've ever had?",
                "Have you ever been caught picking your nose?",
                "What is the most annoying habit you have?",
                "What is your favorite TV show binge-watching guilty pleasure?",
                "Have you ever eavesdropped on a conversation?",
                "What is your most irrational fear?",
                "Have you ever snooped through someone else's phone?",
                "What is the most embarrassing thing you've searched for online?",
                "Have you ever pretended to be sick to get out of something?",
                # Add more non-NSFW truth questions here
            ]
        question = choice(truth_questions)

        embed = Embed(title="Truth", description=question, color=discord.Color.blue())
        if nsfw:
            embed.set_footer(text="**NSFW**")
        await ctx.send(embed=embed)

    @commands.command()
    async def dare(self, ctx, nsfw: bool = False):
        """Get a random dare"""
        if nsfw:
            dares = [
                "masturbate in a voice channel",
                "Give someone a lap dance",
                "Roleplay a steamy scene with a friend",
                "Send a suggestive photo to a friend",
                "Do a body shot off someone",
                "Engage in a naughty chat with a stranger online",
                "Give a sensual massage to someone",
                "Send a seductive message to your crush",
                "Create an adult content account and share the link",
                "Send a dirty secret to someone",
                "Go skinny dipping in a public place",
                "Experiment with a new adult toy and post photos",
                "Take a sensual photo of yourself and share it",
                "Write an erotic story and share it with a friend",
                "Send a provocative voice message to someone",
                "Engage in a virtual intimate encounter",
                "Flirt with a stranger in a voice channel",
                "Send a seductive emoji to the last person you messaged",
                "Create an adult content video and share it with a friend",
                "Give a love bite to someone",
                "Post Nudes in a nsfw channel",
                # Add more NSFW dares here
            ]
        else:
            dares = [
                "Sing a song in a public voice channel",
                "Do 10 push-ups right now",
                "Tell a joke that will make everyone laugh",
                "Wear your clothes backward for the rest of the day",
                "Text your crush and confess your love",
                "Do the chicken dance in a crowded server",
                "Eat a spoonful of a spicy sauce",
                "Speak in a fake accent for the next hour",
                "Do a handstand against a wall",
                "Send a random meme to a friend",
                "Call a friend and sing them a birthday song",
                "Eat a piece of fruit without using your hands",
                "Dance like nobody's watching in a voice channel",
                "Tell a funny story from your childhood",
                "Do 10 jumping jacks right now",
                "Make a funny face and take a selfie",
                "Do a silly walk in your room and share a video",
                "Send a random emoji to the last person you messaged",
                "Write a poem about your favorite food",
                "Post a fun fact in a server you're in",
                # Add more non-NSFW dares here
            ]
        dare = choice(dares)

        embed = Embed(title="Dare", description=dare, color=discord.Color.green())
        if nsfw:
            embed.set_footer(text="**NSFW**")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(TruthOrDare(bot))
