import asyncio
import discord
from redbot.core import commands, Config
import requests
from bs4 import BeautifulSoup
import random

class InteractionsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hug(self, ctx, user: discord.Member):
        gif_url = await self.get_random_anime_gif('anime hug')
        embed = discord.Embed(description=f"{ctx.author.mention} hugged {user.mention}")
        embed.set_image(url=gif_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def kiss(self, ctx, user: discord.Member):
        gif_url = await self.get_random_anime_gif('anime kiss')
        embed = discord.Embed(description=f"{ctx.author.mention} kissed {user.mention}")
        embed.set_image(url=gif_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def slap(self, ctx, user: discord.Member):
        gif_url = await self.get_random_anime_gif('anime slap')
        embed = discord.Embed(description=f"{ctx.author.mention} slapped {user.mention}")
        embed.set_image(url=gif_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def stab(self, ctx, user: discord.Member):
        gif_url = await self.get_random_anime_gif('anime stab')
        embed = discord.Embed(description=f"{ctx.author.mention} stabbed {user.mention}")
        embed.set_image(url=gif_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def punch(self, ctx, user: discord.Member):
        gif_url = await self.get_random_anime_gif('anime punch')
        embed = discord.Embed(description=f"{ctx.author.mention} punched {user.mention}")
        embed.set_image(url=gif_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def kickk(self, ctx, user: discord.Member):
        gif_url = await self.get_random_anime_gif('anime kick')
        embed = discord.Embed(description=f"{ctx.author.mention} kicked {user.mention}")
        embed.set_image(url=gif_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def stomp(self, ctx, user: discord.Member):
        gif_url = await self.get_random_anime_gif('anime stomp')
        embed = discord.Embed(description=f"{ctx.author.mention} stomped on {user.mention}")
        embed.set_image(url=gif_url)
        await ctx.send(embed=embed)

    async def get_random_anime_gif(self, query):
        try:
            search_results = self.google_search(query)
            gif_url = random.choice(search_results)
            return gif_url
        except Exception as e:
            print(f"Error fetching anime GIF: {e}")

    def google_search(self, query):
        url = f"https://www.google.com/search?q={query}&tbm=isch"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        image_elements = soup.find_all("img")
        image_urls = [element["src"] for element in image_elements if element["src"].startswith("http")]
        return image_urls

def setup(bot):
    bot.add_cog(InteractionsCog(bot))

