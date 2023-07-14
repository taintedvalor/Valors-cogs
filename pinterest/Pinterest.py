import discord
from discord.ext import commands
from redbot.core import commands as rb_commands
from redbot.core.utils.menus import DEFAULT_CONTROLS, menu

import requests
from bs4 import BeautifulSoup
import random
import asyncio

class ImageScraperCog(rb_commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.query = None
        self.channel_id = None
        self.interval = 15  # in seconds
        self.bot.loop.create_task(self.start_scraping())

    @rb_commands.command()
    @rb_commands.guild_only()
    async def start(self, ctx, query=None, channel: discord.TextChannel = None):
        """Start the image scraping process."""
        if not query:
            # If no query is provided, use a default query
            query = "cats"
        self.query = query

        if not channel:
            # If no channel is provided, use the current channel
            channel = ctx.channel
        self.channel_id = channel.id

        await ctx.send(f"Image scraping started with query: `{query}`")

    async def start_scraping(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            if self.query and self.channel_id:
                images = await self.scrape_images()
                if images:
                    for image in images:
                        await self.send_image_embed(image)
                        await asyncio.sleep(self.interval)
            await asyncio.sleep(1)

    async def scrape_images(self):
        url = f"https://www.google.com/search?q={self.query}&tbm=isch"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0;Win64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            image_elements = soup.select("img[jsname='HiaYvf']")
            image_urls = [img["src"] for img in image_elements]
            return image_urls
        except requests.exceptions.RequestException as e:
            print(f"Error scraping images: {e}")
            return []

    async def send_image_embed(self, image_url):
        channel = self.bot.get_channel(self.channel_id)
        embed = discord.Embed()
        embed.set_image(url=image_url)
        await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(ImageScraperCog(bot))
