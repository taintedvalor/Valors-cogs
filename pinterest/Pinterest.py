import discord
from redbot.core import commands
import requests
from bs4 import BeautifulSoup
import random
import asyncio

class ImageScrapingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.query = "default query"
        self.channel_id = 1129537678669529209  # Replace with your desired channel ID

    @commands.command()
    async def start(self, ctx, *, query: str = "default query"):
        self.query = query
        await ctx.send(f"Image scraping started with query: {self.query}")
        await self.send_images_periodically()

    async def send_images_periodically(self):
        while True:
            await self.scrape_and_send_image()
            await asyncio.sleep(15)  # Wait for 15 seconds before sending the next image

    async def scrape_and_send_image(self):
        try:
            search_results = self.google_search(self.query)
            image_url = random.choice(search_results)
            embed = discord.Embed()
            embed.set_image(url=image_url)
            
            channel = self.bot.get_channel(self.channel_id)
            await channel.send(embed=embed)
        except Exception as e:
            print(f"Error scraping and sending image: {e}")

    def google_search(self, query):
        url = f"https://www.google.com/search?q={query}&tbm=isch"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        image_elements = soup.find_all("img")
        image_urls = [element["src"] for element in image_elements if element["src"].startswith("http")]
        return image_urls

def setup(bot):
    bot.add_cog(ImageScrapingCog(bot))
