import discord
from discord.ext import commands
import random
from bs4 import BeautifulSoup
import requests
from redbot.core import commands

class PinterestScraper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = None  # Store the channel ID for the configured channel
        self.search_term = None  # Store the search term for Pinterest images
        self.scrape_pinterest.start()

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
        self.search_term = search_term
        await ctx.send(f"Pinterest scraping started with search term: {search_term}.")
    
    @pinterest.command()
    async def stop(self, ctx):
        """Stop the Pinterest image scraping."""
        self.search_term = None
        await ctx.send("Pinterest scraping stopped.")

    @tasks.loop(seconds=15)
    async def scrape_pinterest(self):
        if self.channel_id is not None and self.search_term is not None:
            channel = self.bot.get_channel(self.channel_id)
            if channel is not None:
                # Scrape Pinterest for the specified search term
                pinterest_url = f"https://www.pinterest.com/search/pins/?q={self.search_term}"
                response = requests.get(pinterest_url)
                soup = BeautifulSoup(response.text, 'html.parser')
                image_elements = soup.find_all('img')
                random_image = random.choice(image_elements)

                # Create an embed with the image link
                embed = discord.Embed()
                embed.set_image(url=random_image['src'])

                # Post the embed in the configured channel
                await channel.send(embed=embed)

    @scrape_pinterest.before_loop
    async def before_scrape_pinterest(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(PinterestScraper(bot))
