from redbot.core import commands, Config
import discord
import requests
from bs4 import BeautifulSoup
import asyncio

class Pinterest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)
        default_guild = {"is_running": False, "category": "default", "interval": 15, "channel": None}
        self.config.register_guild(**default_guild)
        self.session = requests.Session()
        self.post_images.start()

    @commands.group()
    async def pinterest(self, ctx):
        """Automatically pull images and GIFs from Pinterest"""
        pass

    @pinterest.command()
    async def start(self, ctx):
        """Start the Pinterest image/GIF search"""
        is_running = await self.config.guild(ctx.guild).is_running()
        if is_running:
            await ctx.send("Pinterest image/GIF search is already running.")
        else:
            await self.config.guild(ctx.guild).is_running.set(True)
            await ctx.send("Pinterest image/GIF search started.")

    @pinterest.command()
    async def stop(self, ctx):
        """Stop the Pinterest image/GIF search"""
        is_running = await self.config.guild(ctx.guild).is_running()
        if not is_running:
            await ctx.send("Pinterest image/GIF search is not running.")
        else:
            await self.config.guild(ctx.guild).is_running.set(False)
            await ctx.send("Pinterest image/GIF search stopped.")

    @pinterest.command()
    async def setcategory(self, ctx, category):
        """Set the search category for Pinterest"""
        await self.config.guild(ctx.guild).category.set(category)
        await ctx.send(f"Search category set to '{category}'.")

    @pinterest.command()
    async def setinterval(self, ctx, interval):
        """Set the interval (in seconds) for posting images or GIFs"""
        try:
            interval = int(interval)
            if interval < 1:
                await ctx.send("Interval must be a positive integer.")
            else:
                await self.config.guild(ctx.guild).interval.set(interval)
                await ctx.send(f"Interval set to {interval} seconds.")
        except ValueError:
            await ctx.send("Invalid interval. Please provide a positive integer.")

    @pinterest.command()
    async def setchannel(self, ctx, channel: discord.TextChannel):
        """Set the channel for posting images or GIFs"""
        await self.config.guild(ctx.guild).channel.set(channel.id)
        await ctx.send(f"Posting channel set to {channel.mention}.")

    @pinterest.command()
    async def settings(self, ctx):
        """Show the current settings for Pinterest in this guild"""
        is_running = await self.config.guild(ctx.guild).is_running()
        category = await self.config.guild(ctx.guild).category()
        interval = await self.config.guild(ctx.guild).interval()
        channel_id = await self.config.guild(ctx.guild).channel()
        channel_mention = ctx.guild.get_channel(channel_id).mention if channel_id else "Not set"

        settings_info = f"**Settings for Pinterest in this guild:**\n"
        settings_info += f"Is Running: {'Yes' if is_running else 'No'}\n"
        settings_info += f"Category: {category}\n"
        settings_info += f"Interval: {interval} seconds\n"
        settings_info += f"Posting Channel: {channel_mention}\n"

        await ctx.send(settings_info)

    @tasks.loop(seconds=15)
    async def post_images(self):
        for guild in self.bot.guilds:
            is_running = await self.config.guild(guild).is_running()
            interval = await self.config.guild(guild).interval()
            channel_id = await self.config.guild(guild).channel()
            category = await self.config.guild(guild).category()

            if is_running and channel_id:
                channel = guild.get_channel(channel_id)
                if channel is None:
                    continue

                images = self.fetch_pinterest_images(category)

                if not images:
                    await channel.send("No images/GIFs found.")

                for image_url in images:
                    image_data = self.session.get(image_url).content
                    file = discord.File(image_data, filename="pinterest_image.gif" if image_url.endswith(".gif") else "pinterest_image.jpg")
                    await channel.send(file=file)

        await asyncio.sleep(interval)

    def fetch_pinterest_images(self, category):
        search_url = f"https://www.pinterest.com/search/pins/?q={category}"
        response = self.session.get(search_url)
        soup = BeautifulSoup(response.content, "html.parser")
        image_tags = soup.find_all("img")
        image_urls = [img["src"] for img in image_tags if img.get("src")]
        return image_urls

    @post_images.before_loop
    async def before_post_images(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(Pinterest(bot))
