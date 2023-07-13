import discord
from discord.ext import commands
import asyncio
import random
import requests
from bs4 import BeautifulSoup

class Pinterest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.search_query = None
        self.interval = 15  # Default interval of 15 sec
        self.channel = None
        self.task = None

    @commands.group(name='pinterest', invoke_without_command=True)
    async def pinterest_group(self, ctx):
        """Pinterest commands"""
        await ctx.send_help(ctx.command)

    @pinterest_group.command(name='start')
    async def pinterest_start(self, ctx):
        """Starts the automated Pinterest image/GIF search."""
        if self.task is None:
            self.task = self.bot.loop.create_task(self._pinterest_search())
            await ctx.send('Pinterest search started.')
        else:
            await ctx.send('Pinterest search is already running.')

    @pinterest_group.command(name='stop')
    async def pinterest_stop(self, ctx):
        """Stops the automated Pinterest image/GIF search."""
        if self.task is not None:
            self.task.cancel()
            self.task = None
            await ctx.send('Pinterest search stopped.')
        else:
            await ctx.send('Pinterest search is not running.')

    @pinterest_group.command(name='setquery')
    async def pinterest_set_query(self, ctx, *, query):
        """Sets the search query for Pinterest."""
        self.search_query = query
        await ctx.send(f'Search query set to: {query}')

    @pinterest_group.command(name='setinterval')
    async def pinterest_set_interval(self, ctx, interval: int):
        """Sets the interval (in seconds) for posting images or GIFs."""
        if interval < 10:
            await ctx.send('Interval should be at least 10 seconds.')
        else:
            self.interval = interval
            await ctx.send(f'Interval set to: {interval} seconds')

    @pinterest_group.command(name='setchannel')
    async def pinterest_set_channel(self, ctx, channel: discord.TextChannel):
        """Sets the channel for posting images or GIFs."""
        self.channel = channel
        await ctx.send(f'Channel set to: {channel.mention}')

    @pinterest_group.command(name='settings')
    async def pinterest_settings(self, ctx):
        """Shows the current settings for Pinterest in the current guild."""
        query = self.search_query or 'Not set'
        interval = self.interval
        channel = self.channel or 'Not set'
        embed = discord.Embed(title='Pinterest Settings', color=discord.Color.blue())
        embed.add_field(name='Search Query', value=query, inline=False)
        embed.add_field(name='Interval (seconds)', value=interval, inline=False)
        embed.add_field(name='Channel', value=channel, inline=False)
        await ctx.send(embed=embed)

    async def _pinterest_search(self):
        while True:
            if self.search_query and self.channel:
                image_url = await self._scrape_pinterest()
                if image_url:
                    embed = discord.Embed(color=discord.Color.blue())
                    embed.set_image(url=image_url)
                    await self.channel.send(embed=embed)
            await asyncio.sleep(self.interval)

    async def _scrape_pinterest(self):
        try:
            url = f'https://www.pinterest.com/search/pins/?q={self.search_query}&rs=typed'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            pins = soup.find_all('a', {'class': 'pinImageWrapper'})
            if pins:
                pin = random.choice(pins)
                image_url = pin.find('img').get('src')
                return image_url
            else:
                return None
        except Exception as e:
            print(f'Pinterest scraping error: {e}')
            return None

def setup(bot):
    bot.add_cog(Pinterest(bot))
