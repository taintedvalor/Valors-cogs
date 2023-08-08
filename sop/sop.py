import discord
from redbot.core import commands
import random
import praw

class SmashOrPass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = {}
        self.reddit = praw.Reddit(
            client_id='BRjqCTnhB_76_ucTXV4J9A',
            client_secret='8lU5K417dv97YjqZ1VBqgxwQVEIoFw',
            user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        )

    @commands.group()
    async def smashorpass(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid subcommand. Use `!help smashorpass` for assistance.")

    @smashorpass.command()
    async def start(self, ctx, term, num_rounds=10, nsfw=False):
        if not ctx.channel.is_nsfw() and nsfw:
            await ctx.send("This command can only be used in NSFW channels.")
            return

        images = self.get_images_from_reddit(term, num_rounds)  # Implement this function
        if not images:
            await ctx.send("No images found.")
            return

        self.games[ctx.channel.id] = {'images': images, 'index': 0, 'votes': {}, 'rounds': num_rounds}
        await self.show_image(ctx)

    async def show_image(self, ctx):
        game_data = self.games[ctx.channel.id]
        if game_data['index'] >= game_data['rounds']:
            await self.end_game(ctx)
            return

        image_url = game_data['images'][game_data['index']]
        message = await ctx.send(f"Smash or Pass: {image_url}\nReact with 👍 to Smash or 👎 to Pass.")
        await message.add_reaction("👍")
        await message.add_reaction("👎")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return
        game_data = self.games[reaction.message.channel.id]
        if reaction.emoji == "👍" or reaction.emoji == "👎":
            game_data['votes'][game_data['index']] = reaction.emoji
            game_data['index'] += 1
            await self.show_image(reaction.message.channel)

    async def end_game(self, ctx):
        game_data = self.games[ctx.channel.id]
        # Display voting results
        result_text = "Voting Results:\n"
        for idx, vote in game_data['votes'].items():
            result_text += f"Round {idx + 1}: {vote}\n"
        await ctx.send(result_text)

        # Clean up
        del self.games[ctx.channel.id]

    def get_images_from_reddit(self, term, num_images):
        subreddit = self.reddit.subreddit('all')  # You can change to a specific subreddit
        images = []
        for submission in subreddit.search(query=term, sort='top', limit=num_images):
            if submission.url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                images.append(submission.url)
        return images

def setup(bot):
    bot.add_cog(SmashOrPass(bot))
