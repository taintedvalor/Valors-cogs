from redbot.core import commands, Config
import discord
import requests
from bs4 import BeautifulSoup
import asyncio
from discord.ext import tasks

class PinterestCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)  # Replace with a unique identifier
        default_guild = {
            "channel": None,
            "query": None,
            "loop_started": False
        }
        self.config.register_guild(**default_guild)
        self.pinterest_loop.start()

    def cog_unload(self):
        self.pinterest_loop.cancel()

    @tasks.loop(seconds=15.0)
    async def pinterest_loop(self):
        for guild_id in await self.config.all_guilds():
            guild = self.bot.get_guild(guild_id)
            if guild:
                async with self.config.guild(guild).all() as guild_config:
                    query = guild_config["query"]
                    channel_id = guild_config["channel"]
                    loop_started = guild_config["loop_started"]
                    
                    if loop_started and query and channel_id:
                        channel = guild.get_channel(channel_id)
                        if channel:
                            url = f"https://www.pinterest.com/search/pins/?q={query}"
                            response = requests.get(url)
                            soup = BeautifulSoup(response.text, "html.parser")
                            images = soup.find_all("img")
                            
                            for image in images:
                                if image.has_attr("src"):
                                    image_url = image["src"]
                                    if image_url.startswith("https://i.pinimg.com"):
                                        embed = discord.Embed()
                                        if image_url.endswith((".gif", ".gifv")):
                                            embed.set_image(url=image_url)
                                        else:
                                            embed.set_thumbnail(url=image_url)
                                        await channel.send(embed=embed)
                                        break

    @commands.group()
    async def pinterest(self, ctx):
        """Pinterest image-related commands."""
        pass

    @pinterest.command()
    async def query(self, ctx, query: str):
        """Set the query for Pinterest image search."""
        await self.config.guild(ctx.guild).query.set(query)
        await ctx.send(f"The query for Pinterest image search has been set to: {query}")

    @pinterest.command()
    async def start(self, ctx):
        """Start sending images from Pinterest."""
        loop_started = await self.config.guild(ctx.guild).loop_started()
        if loop_started:
            await ctx.send("The Pinterest image loop is already running.")
        else:
            channel_id = await self.config.guild(ctx.guild).channel()
            if not channel_id:
                await ctx.send("The designated channel for Pinterest images and GIFs is not set.")
            else:
                await self.config.guild(ctx.guild).loop_started.set(True)
                self.pinterest_loop.start()
                await ctx.send("Pinterest image loop started.")

    @pinterest.command()
    async def stop(self, ctx):
        """Stop sending images from Pinterest."""
        loop_started = await self.config.guild(ctx.guild).loop_started()
        if loop_started:
            await self.config.guild(ctx.guild).loop_started.set(False)
            self.pinterest_loop.stop()
            await ctx.send("Pinterest image loop stopped.")
        else:
            await ctx.send("The Pinterest image loop is not currently running.")

    @commands.is_owner()
    @pinterest.command(name="channel")
    async def set_channel(self, ctx, channel: discord.TextChannel):
        """Set the designated guild channel to send Pinterest images and GIFs."""
        await self.config.guild(ctx.guild).channel.set(channel.id)
        await ctx.send(f"The designated channel for Pinterest images and GIFs has been set to {channel.mention}.")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await self.config.clear_all()

def setup(bot):
    bot.add_cog(PinterestCog(bot))
