import discord
from redbot.core import commands, Config
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
        self.nsfw_timeout = 30  # Time in seconds to wait for user confirmation
        self.config = Config.get_conf(self, identifier=1234567890)  # Replace with a unique identifier

        default_guild_settings = {
            "channel_id": None,
            "interval": 15,
            "nsfw_words": ["nsfw", "18+", "explicit"],
            "last_query_nsfw": False
        }

        self.config.register_guild(**default_guild_settings)

    @commands.group()
    async def autopic(self, ctx):
        """Automatic picture scraping and posting."""
        if ctx.invoked_subcommand is None:
            await ctx.send("hello its ah me?")

    @autopic.command(name="start")
    async def start_autopic(self, ctx, *, query: str = "default query"):
        self.query = query
        if self.channel_id is None:
            self.channel_id = ctx.channel.id
            await ctx.send(f"Image scraping started with query: {self.query} in this channel.")
        else:
            channel = self.bot.get_channel(self.channel_id)
            await ctx.send(f"Image scraping started with query: {self.query} in channel {channel.mention}.")
        await self.send_images_periodically(ctx.guild)

    @autopic.command(name="setchannel")
    async def set_autopic_channel(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            self.channel_id = ctx.channel.id
            await ctx.send("Channel for autopic set to this channel.")
        else:
            self.channel_id = channel.id
            await ctx.send(f"Channel for autopic set to {channel.mention}.")
        await self.save_guild_settings(ctx.guild)

    @autopic.command(name="stop")
    async def stop_autopic(self, ctx):
        self.query = "default query"
        self.channel_id = None
        await ctx.send("Image scraping stopped.")
        await self.save_guild_settings(ctx.guild)

    @autopic.command(name="interval")
    async def set_autopic_interval(self, ctx, seconds: int):
        self.interval = seconds
        await ctx.send(f"Autopic interval set to {seconds} seconds.")
        await self.save_guild_settings(ctx.guild)

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
        await self.save_guild_settings(ctx.guild)

    @autopic.command(name="settings")
    async def view_guild_settings(self, ctx):
        guild_settings = await self.config.guild(ctx.guild).all()
        channel = self.bot.get_channel(guild_settings["channel_id"])
        nsfw_words = ", ".join(guild_settings["nsfw_words"])
        await ctx.send(f"Autopic settings for this guild:\n"
                       f"Channel: {channel.mention if channel else 'Not set'}\n"
                       f"Interval: {guild_settings['interval']} seconds\n"
                       f"NSFW words: {nsfw_words}")

    async def send_images_periodically(self, guild):
        while True:
            await self.scrape_and_send_image(guild)
            await asyncio.sleep(self.interval)

    async def scrape_and_send_image(self, guild):
        try:
            search_results = self.google_search(self.query)
            image_url = random.choice(search_results)
            embed = discord.Embed()
            embed.set_image(url=image_url)

            channel_id = await self.config.guild(guild).channel_id()
            channel = self.bot.get_channel(channel_id)
            last_query_nsfw = await self.config.guild(guild).last_query_nsfw()

            if await self.check_nsfw_words(self.query):
                if not last_query_nsfw:
                    await self.send_nsfw_confirmation(channel, embed, guild)
                else:
                    await asyncio.sleep(self.interval)
            else:
                await channel.send(embed=embed)
                await self.config.guild(guild).last_query_nsfw.set(False)
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

    async def send_nsfw_confirmation(self, channel, embed, guild):
        confirmation_message = await channel.send("Are you sure you want to post this image? It may contain NSFW content. Reply with 'yes' to confirm.")
        try:
            def check_author(message):
                return message.author == self.bot.user

            def check_content(message):
                return message.content.lower() == "yes" and message.channel == channel

            await self.bot.wait_for("message", check=check_content, timeout=self.nsfw_timeout)
            await channel.send(embed=embed)
            await self.config.guild(guild).last_query_nsfw.set(False)
        except asyncio.TimeoutError:
            await confirmation_message.delete()
            await self.config.guild(guild).last_query_nsfw.set(True)

    async def save_guild_settings(self, guild):
        await self.config.guild(guild).channel_id.set(self.channel_id)
        await self.config.guild(guild).interval.set(self.interval)
        await self.config.guild(guild).nsfw_words.set(self.nsfw_words)

def setup(bot):
    bot.add_cog(autopic(bot))
