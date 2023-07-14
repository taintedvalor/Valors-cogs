import discord
from discord.ext import tasks
import random
from bs4 import BeautifulSoup
import requests
from redbot.core import commands

class PinterestScraper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = None  # Store the channel ID for the configured channel

    @commands.group()
    async def pinterest(self, ctx):
        """Pinterest image scraper commands."""
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid command. Use `pinterest help` for more information.")

    @pinterest.command()
    async def set_channel(self, ctx, channel: discord.TextChannel):
        """Set the channel to post the Pinterest images."""
        self.channel_id = channel.id
        await ctx.send(f"Channel set to {channel.mention}.")

    @pinterest.command()
    async def start(self, ctx, *, search_term: str):
        """Start the Pinterest image scraping."""
        if self.channel_id is None:
            await ctx.send("Channel not set. Use the `pinterest set_channel` command first.")
            return

        pinterest_url = f"https://www.pinterest.com/search/pins/?q={search_term}"
        response = requests.get(pinterest_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        image_elements = soup.find_all('img')
        
        if not image_elements:
            await ctx.send("No images found for the specified search term.")
            return
        
        random_image = random.choice(image_elements)
        image_url = random_image['src']

        channel = self.bot.get_channel(self.channel_id)
        if channel is not None:
            embed = discord.Embed()
            embed.set_image(url=image_url)

            await channel.send(embed=embed)
            await ctx.send("Image sent to the configured channel.")
        else:
            await ctx.send("Invalid channel. Make sure the bot has access to the specified channel.")

def setup(bot):
    bot.add_cog(PinterestScraper(bot))
