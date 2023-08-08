import random
import discord
from discord.ext import commands
from redbot.core import Config

class SmashOrPass(commands.Cog):
    """Play the Smash or Pass game."""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=806715409318936617)
        default_guild = {
            "searchTerm": "random",
            "imageAmount": 10,
            "cleanup": False
        }
        self.config.register_guild(**default_guild)

    @commands.group()
    async def smashorpass(self, ctx):
        """Play the Smash or Pass game."""
        pass

    @smashorpass.command(name="config")
    async def sop_config(self, ctx, amount: int = 10, *, search_term: str = "random"):
        """Configure the Smash or Pass game settings."""
        await self.config.guild(ctx.guild).searchTerm.set(search_term)
        await self.config.guild(ctx.guild).imageAmount.set(amount)
        await ctx.send(f"Smash or Pass game settings updated: Search term = '{search_term}', Image amount = {amount}")

    @smashorpass.command(name="play")
    async def sop_play(self, ctx):
        """Play the Smash or Pass game."""
        search_term = await self.config.guild(ctx.guild).searchTerm()
        image_amount = await self.config.guild(ctx.guild).imageAmount()
        cleanup_enabled = await self.config.guild(ctx.guild).cleanup()

        searchEngines = [
            {
                "title": "Google",
                "url": "https://www.google.com/search?hl=en&q="
            },
            {
                "title": "Bing",
                "url": "https://www.bing.com/images/search?q="
            },
            # Add more search engines here...
        ]

        random_search_engine = random.choice(searchEngines)
        query = search_term if search_term != "random" else "random"
        search_url = random_search_engine["url"] + query
        images = get_random_images(search_url, image_amount)

        for image in images:
            embed = discord.Embed(title="Smash or Pass", description=f"React with 👍 to smash or 👎 to pass!\nImage URL: {image}")
            message = await ctx.send(embed=embed)
            await message.add_reaction("👍")
            await message.add_reaction("👎")

        def check(reaction, user):
            return user != self.bot.user and reaction.message.id == message.id and str(reaction.emoji) in ["👍", "👎"]

        smash_count = 0
        pass_count = 0
        while True:
            try:
                reaction, _ = await self.bot.wait_for("reaction_add", timeout=60, check=check)
            except asyncio.TimeoutError:
                break
            if str(reaction.emoji) == "👍":
                smash_count += 1
            elif str(reaction.emoji) == "👎":
                pass_count += 1
            await reaction.remove(ctx.author)

        result_embed = discord.Embed(title="Smash or Pass Results", description=f"Smash: {smash_count}\nPass: {pass_count}")
        await ctx.send(embed=result_embed)

        if cleanup_enabled:
            await ctx.channel.delete_messages([message] + await ctx.channel.history().flatten())

def setup(bot):
    bot.add_cog(SmashOrPass(bot))
