import discord
from redbot.core import commands, Config, checks
import asyncio
import requests

class PinterestCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)
        default_settings = {
            "query_interval": 15,  # in seconds
            "channel_id": None,
            "query": None
        }
        self.config.register_guild(**default_settings)
        self.query_task = None

    @commands.command()
    @commands.guild_only()
    @checks.admin()
    async def pinterest_query(self, ctx, query: str):
        """Starts sending Pinterest images based on the specified query."""
        if self.query_task:
            await ctx.send("A Pinterest query is already running. Use `[p]pinterest_stop` to stop it.")
            return

        await self.config.guild(ctx.guild).query_interval.set(15)
        await self.config.guild(ctx.guild).channel_id.set(ctx.channel.id)
        await self.config.guild(ctx.guild).query.set(query)
        self.query_task = self.bot.loop.create_task(self.send_images_task(ctx.guild))
        await ctx.send(f"Started Pinterest query for '{query}'.")

    @commands.command()
    @commands.guild_only()
    @checks.admin()
    async def pinterest_stop(self, ctx):
        """Stops the currently running Pinterest query."""
        if self.query_task:
            self.query_task.cancel()
            self.query_task = None
            await ctx.send("Stopped the Pinterest query.")
        else:
            await ctx.send("No Pinterest query is currently running.")

    async def send_images_task(self, guild):
        while True:
            if self.query_task is None:
                break

            query_interval = await self.config.guild(guild).query_interval()
            channel_id = await self.config.guild(guild).channel_id()
            query = await self.config.guild(guild).query()

            image_url = self.get_pinterest_image(query)
            if image_url:
                channel = self.bot.get_channel(channel_id)
                await channel.send(image_url)

            await asyncio.sleep(query_interval)

    def get_pinterest_image(self, query):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        url = f"https://www.pinterest.com/search/pins/?q={query}&rs=typed"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # Parse the response HTML and extract the image URL
            # You may need to use a different method depending on the structure of the Pinterest page
            # Here's an example using BeautifulSoup
            from bs4 import BeautifulSoup

            soup = BeautifulSoup(response.content, "html.parser")
            image_element = soup.select_one("img[src^='https://i.pinimg.com/']")
            if image_element:
                return image_element["src"]

        return None

def setup(bot):
    bot.add_cog(PinterestCog(bot))
