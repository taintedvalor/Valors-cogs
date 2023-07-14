import discord
from redbot.core import commands
import requests
from bs4 import BeautifulSoup
import random
import asyncio

class autopic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.query = "default query"
        self.channel_id = None
        self.interval = 15
        self.nsfw_words = ["nsfw", "18+", "explicit"]  # List of NSFW words

    @commands.group()
    async def autopic(self, ctx):
        """Automatic picture scraping and posting."""
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid subcommand for autopic.")

    @autopic.command(name="start")
    async def start_autopic(self, ctx, *, query: str = "default query"):
        self.query = query
        if self.channel_id is None:
            self.channel_id = ctx.channel.id
            await ctx.send(f"Image scraping started with query: {self.query} in this channel a channel was not set yet.")
        else:
            channel = self.bot.get_channel(self.channel_id)
            await ctx.send(f"Image scraping started with query: {self.query} in channel {channel.mention}.")
        await self.send_images_periodically()

    @autopic.command(name="setchannel")
    async def set_autopic_channel(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            self.channel_id = ctx.channel.id
            await ctx.send("Channel for autopic set to this channel.")
        else:
            self.channel_id = channel.id
            await ctx.send(f"Channel for autopic set to {channel.mention}.")

    @autopic.command(name="stop")
    async def stop_autopic(self, ctx):
        self.query = "default query"
        self.channel_id = None
        await ctx.send("Image scraping stopped.")

    @autopic.command(name="interval")
    async def set_autopic_interval(self, ctx, seconds: int):
        self.interval = seconds
        await ctx.send(f"Autopic interval set to {seconds} seconds.")

    @autopic.command(name="nsfwlist")
    async def modify_nsfw_list(self, ctx, action: str, *, word: str):
        if action.lower() == "add":
            self.nsfw_words.append(word)
            await ctx.send(f"Added '{word}' to the NSFW word list.")
        elif action.lower() == "remove":
            if word in self.nsfw_words:
                self.nsfw_words.remove(word)
                await ctx.send(f"Removed '{word}' from the NSFW word list.")
            else:
                await ctx.send(f"'{word}' is not in the NSFW word list.")
        else:
            await ctx.send("Invalid action. Use 'add' or 'remove'.")

    async def send_images_periodically(self):
        while True:
            await self.scrape_and_send_image()
            await asyncio.sleep(self.interval)

    async def scrape_and_send_image(self):
        try:
            search_results = self.google_search(self.query)
            image_url = random.choice(search_results)
            embed = discord.Embed()
            embed.set_image(url=image_url)

            channel = self.bot.get_channel(self.channel_id)
            if await self.check_nsfw_words(self.query):
                await channel.send("Are you sure you want to post this image? It may contain NSFW content.", embed=embed)
            else:
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

    async def check_nsfw_words(self, query):
        for word in self.nsfw_words:
            if word in query.lower():
                return True
        return False

def setup(bot):
    bot.add_cog(autopic(bot))
