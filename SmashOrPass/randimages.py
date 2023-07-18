import discord
from redbot.core import checks, commands
from redbot.core.i18n import Translator, cog_i18n

from .core import Core
from . import constants as sub

_ = Translator("Image", __file__)

class SmashOrPass(red_commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rounds = 0
        self.answers = {}
        self.image_cog = Core(bot)  # Instantiate the Core class for image fetching

    @red_commands.cooldown(1, 5, red_commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command()
    async def smashorpass(self, ctx):
        """Play a game of Smash or Pass."""
        if self.rounds >= 10:
            await ctx.send("The game has already ended.")
            return

        # Fetch a random wallpaper image from subreddits
        image_url = await self.fetch_random_wallpaper()

        # Send the image and reaction prompt
        embed = discord.Embed(title="Smash or Pass", description="React with :heart: for Smash or :no_entry: for Pass.")
        embed.set_image(url=image_url)
        message = await ctx.send(embed=embed)
        await message.add_reaction("❤️")
        await message.add_reaction("⛔")

        def check(reaction, user):
            return user == ctx.author and reaction.message.id == message.id and str(reaction.emoji) in ["❤️", "⛔"]

        try:
            reaction, _ = await self.bot.wait_for("reaction_add", timeout=60.0, check=check)
        except TimeoutError:
            await ctx.send("No reaction received. Aborting game.")
            return

        # Record the answer
        emoji = str(reaction.emoji)
        self.answers[ctx.author.id] = emoji
        self.rounds += 1

        # End the game after 10 rounds
        if self.rounds == 10:
            await self.display_results(ctx)
            self.rounds = 0
            self.answers = {}

    async def fetch_random_wallpaper(self):
        # Fetch a random wallpaper image from subreddits using the Core cog
        # Replace this with your own implementation
        image_url = await self.image_cog._send_reddit_msg(
            None,
            name="a wallpaper",
            emoji="🖼️",
            sub=sub.WALLPAPERS,
            details=True,
        )
        return image_url

    async def display_results(self, ctx):
        # Create an embed with the game results
        embed = discord.Embed(title="Smash or Pass Results", description="Here are the results of the game:")

        for user_id, answer in self.answers.items():
            user = ctx.guild.get_member(user_id)
            if user:
                embed.add_field(name=user.display_name, value=answer, inline=False)
            else:
                embed.add_field(name="Unknown User", value=answer, inline=False)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(SmashOrPass(bot))

