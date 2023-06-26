import discord
from redbot.core import commands
from random import choice

class TruthOrDare(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def truth(self, ctx):
        """Get a random truth question"""
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
            # Add more truth questions here
        ]
        question = choice(truth_questions)
        await ctx.send(f"Truth: {question}")

    @commands.command()
    async def dare(self, ctx):
        """Get a random dare"""
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
            # Add more dares here
        ]
        dare = choice(dares)
        await ctx.send(f"Dare: {dare}")

def setup(bot):
    bot.add_cog(TruthOrDare(bot))
