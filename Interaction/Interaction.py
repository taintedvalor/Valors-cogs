import discord
from redbot.core import commands, Config
import requests
from bs4 import BeautifulSoup
import random
import imageio
import time
import os

class InteractionsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hug(self, ctx, user: discord.Member):
        gif_path = await self.get_random_anime_gif('anime hug')
        await self.display_gif(ctx, gif_path, f"{ctx.author.mention} hugged {user.mention}")

    @commands.command()
    async def kiss(self, ctx, user: discord.Member):
        gif_path = await self.get_random_anime_gif('anime kiss')
        await self.display_gif(ctx, gif_path, f"{ctx.author.mention} kissed {user.mention}")

    @commands.command()
    async def slap(self, ctx, user: discord.Member):
        gif_path = await self.get_random_anime_gif('anime slap')
        await self.display_gif(ctx, gif_path, f"{ctx.author.mention} slapped {user.mention}")

    @commands.command()
    async def stab(self, ctx, user: discord.Member):
        gif_path = await self.get_random_anime_gif('anime stab')
        await self.display_gif(ctx, gif_path, f"{ctx.author.mention} stabbed {user.mention}")

    @commands.command()
    async def punch(self, ctx, user: discord.Member):
        gif_path = await self.get_random_anime_gif('anime punch')
        await self.display_gif(ctx, gif_path, f"{ctx.author.mention} punched {user.mention}")

    @commands.command()
    async def kickk(self, ctx, user: discord.Member):
        gif_path = await self.get_random_anime_gif('anime kick')
        await self.display_gif(ctx, gif_path, f"{ctx.author.mention} kicked {user.mention}")

    @commands.command()
    async def stomp(self, ctx, user: discord.Member):
        gif_path = await self.get_random_anime_gif('anime stomp')
        await self.display_gif(ctx, gif_path, f"{ctx.author.mention} stomped on {user.mention}")

    async def get_random_anime_gif(self, query):
        try:
            search_results = self.google_search(query)
            gif_url = random.choice(search_results)
            gif_path = await self.download_gif(gif_url)
            return gif_path
        except Exception as e:
            print(f"Error fetching anime GIF: {e}")

    def google_search(self, query):
        url = f"https://www.google.com/search?q={query}&tbm=isch"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        image_elements = soup.find_all("img")
        image_urls = [element["src"] for element in image_elements if element["src"].startswith("http")]
        return image_urls

    async def download_gif(self, url):
        response = requests.get(url, stream=True)
        response.raise_for_status()
        gif_path = "temp.gif"  # Path to temporarily save the GIF
        with open(gif_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        return gif_path

    async def display_gif(self, ctx, gif_path, description):
        gif = imageio.mimread(gif_path)
        for i, frame in enumerate(gif):
            frame_path = f"frame_{i}.gif"
            imageio.imwrite(frame_path, frame, format='GIF-FI')  # Save the frame as a separate GIF file
            frame_file = discord.File(frame_path, filename=frame_path)  # Create a file object from the frame file
            embed = discord.Embed(description=description)
            embed.set_image(url=f"attachment://{frame_path}")
            await ctx.send(embed=embed, file=frame_file)
            os.remove(frame_path)  # Remove the frame file after sending it

        os.remove(gif_path)  # Remove the temporary GIF file

def setup(bot):
    bot.add_cog(InteractionsCog(bot))
