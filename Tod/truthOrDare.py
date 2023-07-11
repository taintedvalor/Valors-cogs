import discord
from redbot.core import commands
import random
import asyncio

class TruthOrDare(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tod(self, ctx):
        messages = {
            "truth": [
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
                "Do you have a favourite sibling?",
                "What have you bought that's been the biggest waste of money?",
                "What is a secret you have never told anyone?",
                "Do you have a hidden talent?",
                "If you could swap lives with someone in the room, who would it be?",
                "Do you have a favourite friend?",
                "Name someone you've pretended to like but actually couldn't stand.",
                "If you could become invisible, what's the worst thing you'd do?",
                "What's the worst thing you've ever done at work?",
                "Rate everyone playing from your most to least favourite.",
                "What is your most absurd dealbreaker?",
                "Have you ever broken the law?",
                "If you had to get back with an ex, who would you choose?",
                "Who would you call in the room to help bury a body?",
                "Who is the most surprising person to ever slide into your DMs?",
                "What is something you're glad your mum doesn't know about you?",
                "Have you ever gone skinny dipping?",
                "What's the one thing you'd never do for all the money in the world?",
                "Who do you think is the worst dressed person in the room?",
                "Who in the room would be the worst person to date and why?",
            ],
            "dare": [
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
                "ping typical_pigeon and tell him what a nice guy he is",
                "Let another person post a status on your behalf.",
                "Take a selfie with 5 different bouncers.",
                "Let the other players go through your phone for one minute.",
                "Photobomb a picture.",
                "Get an item from the bathroom and sell it to the group for 3 minutes.",
                "Let another person draw a tattoo on your back with a permanent marker.",
                "Drink a mystery drink created by the rest of the group.",
                "Show your search history on your phone.",
                "Let the rest of the group DM someone from your Instagram.",
                "Keep 3 ice cubes in your mouth until they melt.",
                "Yell out the first word that comes to your mind.",
                "Pretend to be the person on your left for 10 minutes.",
                "Whisper a secret to the person on your left.",
                "Eat something of the group's choice without using your hands.",
                "Let another person in the group touch up your makeup.",
                "Say two honest things about everyone in the group.",
                "Talk in an American or Australian accent for the next 10 minutes.",
                "Scroll through your Instagram followers until someone says stop, and you have to like all their pics.",
                "Let someone shave a part of your body.",
                "Reply to the first five Instagram stories on your timeline.",
                "Steal a duck from your local pond",
                "go to sleep",
            ],
            "nsfw_truth": [
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
                "Post a video of you trying to suck your own dick in an nsfw channel",
                "What's your biggest turn off?",
                "What's the largest age gap between you and your sexual partners?",
                "Does size really matter?",
                "Who was your worst sexual partner and why?",
                "Have you ever faked an orgasm?",
                "Have you ever been caught in action? If so, by who?",
                "If you could only ever do one position for the rest of your life, which one would it be and why?",
                "What's the most embarrassing thing that's happened to you during sex?",
                "Where's the riskiest place you've done it?",
                "Have you ever filmed a sex tape?",
                "What's your biggest turn on?",
                "Do you have any fetishes?",
                "Do you like loud or silent people in bed?",
                "What is your favourite song when it comes to action in the bedroom?",
                "What's your maddest one-night stand story?",
            ],
            "nsfw_dare": [
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
                "What's your biggest turn off?",
                "What's the largest age gap between you and your sexual partners?",
                "Does size really matter?",
                "Who was your worst sexual partner and why?",
                "Have you ever faked an orgasm?",
                "Have you ever been caught in action? If so, by who?",
                "If you could only ever do one position for the rest of your life, which one would it be and why?",
                "What's the most embarrassing thing that's happened to you during sex?",
                "Have you ever filmed a sex tape?",
                "What's your biggest turn on?",
                "Do you have any fetishes?",
                "Do you like loud or silent people in bed?",
                "What is your favourite song when it comes to action in the bedroom?",
                "What's your maddest one-night stand story?",
                "Send your ex a message saying you miss them.",
                "Make eye contact with the person to your right and moan for 10 seconds.",
                "Ask a stranger for advice on a strange rash you've recently developed.",
                "Make your orgasm face at the next stranger you see until they make eye contact with you.",
                "Seductively eat a banana whilst locking eyes with the person to your left.",
                "Send one of your parents a sext and don't reply to them for one hour.",
                "Pass your phone to the person on your left and let them post a sexual status to your Facebook.",
                "Perform a seductive dance in front of the group.",
                "Pick up the nearest object to you and demonstrate how to put on protection.",
                "Close your eyes, pick a random phone contact and leave them a dirty voicemail.",
                "Drop an ice cube in your pants.",
                "Google the dirtiest thing you can think of and show it to the person next to you.",
                "FaceTime your most recent contact, burp, then hang up.",
                "Smell everyone's armpits and rank them from best to worst.",
                "Tell us the one bedtime secret no one knows about you.",
            ],
        }

        async def send_question(embed_title, embed_description):
            embed = discord.Embed(title=embed_title, description=embed_description)
            await ctx.send(embed=embed)

        truth_emoji = "🔍"
        dare_emoji = "🎯"
        nsfw_emoji = "🔞"

        message = await ctx.send(embed=discord.Embed(title="Truth or Dare", description="Click an emoji to get a random question:\n"
                                                                                      f"{truth_emoji} - Truth\n"
                                                                                      f"{dare_emoji} - Dare\n"
                                                                                      f"{nsfw_emoji} - NSFW Question"))
        await message.add_reaction(truth_emoji)  # Truth
        await message.add_reaction(dare_emoji)  # Dare
        await message.add_reaction(nsfw_emoji)  # NSFW

        def reaction_check(reaction, user):
            return (
                user == ctx.author
                and reaction.message.id == message.id
                and str(reaction.emoji) in [truth_emoji, dare_emoji, nsfw_emoji]
            )

        while True:
            try:
                reaction, _ = await self.bot.wait_for(
                    "reaction_add", check=reaction_check, timeout=120.0
                )
            except asyncio.TimeoutError:
                await ctx.send("timed out origin messages removed.")
                await message.delete()
                break

            if str(reaction.emoji) == truth_emoji:
                random_message = random.choice(messages["truth"])
                await send_question("Random Truth Question", random_message)
            elif str(reaction.emoji) == dare_emoji:
                random_message = random.choice(messages["dare"])
                await send_question("Random Dare Question", random_message)
            elif str(reaction.emoji) == nsfw_emoji:
                nsfw_reactions = ["💣", "💥"]  # NSFW reactions to swap to
                if ctx.channel.is_nsfw():
                    nsfw_message = await ctx.send(embed=discord.Embed(title="Random NSFW Question", description="Click an emoji to get a random NSFW question:\n"
                                                                                                                  f"{nsfw_reactions[0]} - NSFW Truth\n"
                                                                                                                  f"{nsfw_reactions[1]} - NSFW Dare"))
                    await nsfw_message.add_reaction(nsfw_reactions[0])  # NSFW Truth
                    await nsfw_message.add_reaction(nsfw_reactions[1])  # NSFW Dare

                    def nsfw_reaction_check(nsfw_reaction, nsfw_user):
                        return (
                            nsfw_user == ctx.author
                            and nsfw_reaction.message.id == nsfw_message.id
                            and str(nsfw_reaction.emoji) in nsfw_reactions
                        )

                    while True:
                        try:
                            nsfw_reaction, _ = await self.bot.wait_for(
                                "reaction_add", check=nsfw_reaction_check, timeout=30.0
                            )
                        except asyncio.TimeoutError:
                            await ctx.send("timed out origin messages removed.")
                            await nsfw_message.delete()
                            break

                        if str(nsfw_reaction.emoji) == nsfw_reactions[0]:
                            random_message = random.choice(messages["nsfw_truth"])
                            await send_question("Random NSFW Truth Question", random_message)
                        elif str(nsfw_reaction.emoji) == nsfw_reactions[1]:
                            random_message = random.choice(messages["nsfw_dare"])
                            await send_question("Random NSFW Dare Question", random_message)
                else:
                    confirm_emoji = "✅"
                    cancel_emoji = "❌"

                    confirm_message = await ctx.send(
                        embed=discord.Embed(
                            title="NSFW Command Confirmation",
                            description="This command can only be used in NSFW channels. Do you want to proceed with NSFW questions?",
                        )
                    )
                    await confirm_message.add_reaction(confirm_emoji)
                    await confirm_message.add_reaction(cancel_emoji)

                    def confirm_check(reaction, user):
                        return (
                            user == ctx.author
                            and reaction.message.id == confirm_message.id
                            and str(reaction.emoji) in [confirm_emoji, cancel_emoji]
                        )

                    try:
                        confirm_reaction, _ = await self.bot.wait_for(
                            "reaction_add", check=confirm_check, timeout=30.0
                        )
                    except asyncio.TimeoutError:
                        await ctx.send("timed out origin messages removed.")
                        await confirm_message.delete()
                        break

                    if str(confirm_reaction.emoji) == confirm_emoji:
                        nsfw_message = await ctx.send(embed=discord.Embed(title="Random NSFW Question", description="Click an emoji to get a random NSFW question:\n"
                                                                                                                      f"{nsfw_reactions[0]} - NSFW Truth\n"
                                                                                                                      f"{nsfw_reactions[1]} - NSFW Dare"))
                        await nsfw_message.add_reaction(nsfw_reactions[0])  # NSFW Truth
                        await nsfw_message.add_reaction(nsfw_reactions[1])  # NSFW Dare

                        def nsfw_reaction_check(nsfw_reaction, nsfw_user):
                            return (
                                nsfw_user == ctx.author
                                and nsfw_reaction.message.id == nsfw_message.id
                                and str(nsfw_reaction.emoji) in nsfw_reactions
                            )

                        while True:
                            try:
                                nsfw_reaction, _ = await self.bot.wait_for(
                                    "reaction_add", check=nsfw_reaction_check, timeout=30.0
                                )
                            except asyncio.TimeoutError:
                                await ctx.send("timed out origin messages removed.")
                                await nsfw_message.delete()
                                break

                            if str(nsfw_reaction.emoji) == nsfw_reactions[0]:
                                random_message = random.choice(messages["nsfw_truth"])
                                await send_question("Random NSFW Truth Question", random_message)
                            elif str(nsfw_reaction.emoji) == nsfw_reactions[1]:
                                random_message = random.choice(messages["nsfw_dare"])
                                await send_question("Random NSFW Dare Question", random_message)
                    else:
                        await ctx.send("NSFW command canceled.")

def setup(bot):
    bot.add_cog(TruthOrDare(bot))
