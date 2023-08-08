import discord
from redbot.core import commands
import random

class SmashOrPass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = {}

    @commands.group()
    async def smashorpass(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid subcommand. Use `!help smashorpass` for assistance.")

    @smashorpass.command()
    async def start(self, ctx, term, num_images=10, rounds=10, nsfw=False):
        if not ctx.channel.is_nsfw() and nsfw:
            await ctx.send("This command can only be used in NSFW channels.")
            return

        images = self.get_images_from_search(term, num_images)  # Implement this function
        self.games[ctx.channel.id] = {'images': images, 'index': 0, 'votes': {}, 'rounds': rounds}
        await self.show_image(ctx)

    async def show_image(self, ctx):
        game_data = self.games[ctx.channel.id]
        if game_data['index'] >= len(game_data['images']):
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
            result_text += f"Image {idx + 1}: {vote}\n"
        await ctx.send(result_text)

        # Clean up
        del self.games[ctx.channel.id]

def setup(bot):
    bot.add_cog(SmashOrPass(bot))
