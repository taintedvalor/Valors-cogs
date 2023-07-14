import discord
from discord.ext import tasks
from redbot.core import commands
import requests
from bs4 import BeautifulSoup
import random
import asyncio

class PinterestCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.query = None
        self.channel_id = None
        self.interval = 15  # in seconds
        self.bot.loop.create_task(self.start_searching())

    @commands.command()
    async def pinterest(self, ctx, *, query):
        """Start searching and displaying Pinterest images."""
        self.query = query
        self.channel_id = ctx.channel.id
        await ctx.send(f"Started searching Pinterest for: `{query}`")

    async def start_searching(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            if self.query and self.channel_id:
                images = await self.search_pinterest()
                if images:
                    for image in images:
                        await self.send_image_embed(image)
                        await asyncio.sleep(self.interval)
            await asyncio.sleep(1)

    async def search_pinterest(self):
        url = f"https://www.pinterest.com/search/pins/?q={self.query.replace(' ', '%20')}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        image_elements = soup.select(".GrowthUnauthPinImage")
        image_urls = [element["src"] for element in image_elements]
        return image_urls

    async def send_image_embed(self, image_url):
        channel = self.bot.get_channel(self.channel_id)
        embed = discord.Embed()
        embed.set_image(url=image_url)
        await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(PinterestCog(bot))
