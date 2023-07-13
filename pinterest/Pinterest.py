import discord
from discord.ext import commands, tasks
import random
import aiohttp
from datetime import datetime, timedelta
from redbot.core import commands as rcommands
from redbot.core.bot import Red
import asyncio

class PinterestCog(rcommands.Cog):
    def __init__(self, bot: Red):
        self.bot = bot
        self.settings = {}
        self.search_tasks = {}

    @rcommands.group(name='pinterest', aliases=['pin'], invoke_without_command=True)
    @rcommands.has_permissions(manage_guild=True)
    async def pinterest(self, ctx: rcommands.Context):
        """Pinterest cog commands."""
        await ctx.send_help(ctx.command)

    @pinterest.command(name='start')
    async def start_pinterest_search(self, ctx: rcommands.Context):
        """Starts the automated Pinterest image/GIF search."""
        guild_id = ctx.guild.id
        if guild_id in self.search_tasks:
            await ctx.send("Pinterest search is already running.")
            return

        settings = self.settings.get(guild_id)
        if not settings or not settings.get('query') or not settings.get('interval') or not settings.get('channel'):
            await ctx.send("Please set the search query, interval, and channel before starting.")
            return

        search_task = self.bot.loop.create_task(self._search_pinterest(guild_id))
        self.search_tasks[guild_id] = search_task
        await ctx.send("Pinterest search started.")

    @pinterest.command(name='stop')
    async def stop_pinterest_search(self, ctx: rcommands.Context):
        """Stops the automated Pinterest image/GIF search."""
        guild_id = ctx.guild.id
        search_task = self.search_tasks.get(guild_id)
        if search_task and not search_task.done():
            search_task.cancel()
            del self.search_tasks[guild_id]
            await ctx.send("Pinterest search stopped.")
        else:
            await ctx.send("Pinterest search is not running.")

    @pinterest.command(name='setquery')
    async def set_query(self, ctx: rcommands.Context, *, query: str):
        """Sets the search query for Pinterest."""
        guild_id = ctx.guild.id
        self._ensure_settings(guild_id)
        self.settings[guild_id]['query'] = query
        await ctx.send(f"Search query set to: {query}")

    @pinterest.command(name='setinterval')
    async def set_interval(self, ctx: rcommands.Context, interval: int):
        """Sets the interval (in seconds) for posting images or GIFs."""
        guild_id = ctx.guild.id
        self._ensure_settings(guild_id)
        self.settings[guild_id]['interval'] = interval
        await ctx.send(f"Interval set to: {interval} seconds")

    @pinterest.command(name='setchannel')
    async def set_channel(self, ctx: rcommands.Context, channel: discord.TextChannel):
        """Sets the channel for posting images or GIFs."""
        guild_id = ctx.guild.id
        self._ensure_settings(guild_id)
        self.settings[guild_id]['channel'] = channel
        await ctx.send(f"Channel set to: {channel.mention}")

    @pinterest.command(name='settings')
    async def show_settings(self, ctx: rcommands.Context):
        """Shows the current settings for Pinterest in the current guild."""
        guild_id = ctx.guild.id
        settings = self.settings.get(guild_id, {})
        query = f"Query: {settings.get('query', 'cats')}"
        interval = f"Interval: {settings.get('interval', 15)} seconds"
        channel = f"Channel: {settings.get('channel', 'Not set')}"

        embed = discord.Embed(title="Pinterest Settings", color=discord.Color.blue())
        embed.add_field(name="Query", value=query)
        embed.add_field(name="Interval", value=interval)
        embed.add_field(name="Channel", value=channel)

        await ctx.send(embed=embed)

    async def _search_pinterest(self, guild_id):
        settings = self.settings.get(guild_id, {})
        interval = settings.get('interval', 15)
        channel_id = settings.get('channel')
        channel = self.bot.get_channel(channel_id)
        query = settings.get('query', 'cats')

        while not self.bot.is_closed():
            image_url = await self._get_random_pinterest_image(query)
            if image_url:
                await channel.send(image_url)
            else:
                await channel.send("Unable to find an image or GIF for the current query.")

            await asyncio.sleep(interval)

    async def _get_random_pinterest_image(self, query):
        async with aiohttp.ClientSession() as session:
            url = f"https://www.pinterest.com/search/pins/?q={query}&rs=typed"
            async with session.get(url) as response:
                if response.status == 200:
                    text = await response.text()
                    # Extract image URLs from the response using a suitable method
                    # Modify this part based on your chosen scraping method
                    image_urls = []
                    # Extract image URLs from the response
                    # ...
                    if image_urls:
                        return random.choice(image_urls)
        return None

    def _ensure_settings(self, guild_id):
        if guild_id not in self.settings:
            self.settings[guild_id] = {
                'query': 'cats',
                'interval': 15,
                'channel': None
            }

def setup(bot: Red):
    bot.add_cog(PinterestCog(bot))
