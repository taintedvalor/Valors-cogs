import discord
from discord.ext import commands, tasks
import requests
from bs4 import BeautifulSoup
from redbot.core import commands as red_commands
from redbot.core import Config

class PinterestCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)  # Replace with a unique identifier
        default_guild = {
            "channel": None,
            "query": None
        }
        self.config.register_guild(**default_guild)
        self.pinterest_loop.start()

    def cog_unload(self):
        self.pinterest_loop.cancel()

    @tasks.loop(seconds=15.0)
    async def pinterest_loop(self):
        async with self.config.guild(self.bot.get_guild().id).all() as guild_config:
            query = guild_config["query"]
            channel_id = guild_config["channel"]
            channel = self.bot.get_channel(channel_id)
            
            if query and channel:
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

    @red_commands.group()
    async def pinterest(self, ctx):
        """Pinterest image-related commands."""
        pass

    @pinterest.command()
    async def start(self, ctx, query: str):
        """Start sending images from Pinterest with the specified query."""
        await self.config.guild(ctx.guild).query.set(query)
        self.pinterest_loop.start()
        await ctx.send(f"Pinterest image loop started with query: {query}")

    @pinterest.command()
    async def stop(self, ctx):
        """Stop sending images from Pinterest."""
        await self.config.guild(ctx.guild).query.set(None)
        self.pinterest_loop.stop()
        await ctx.send("Pinterest image loop stopped.")

    @red_commands.is_owner()
    @pinterest.command(name="channel")
    async def set_channel(self, ctx, channel: discord.TextChannel):
        """Set the designated guild channel to send Pinterest images and GIFs."""
        await self.config.guild(ctx.guild).channel.set(channel.id)
        await ctx.send(f"The designated channel for Pinterest images and GIFs has been set to {channel.mention}.")

    @red_commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await self.config.clear_all()

def setup(bot):
    bot.add_cog(PinterestCog(bot))
