import discord
from discord.ext import commands

class VentCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def vent(self, ctx, guild_id: int, *, message):
        guild = self.bot.get_guild(guild_id)
        if guild is None:
            await ctx.send("Target guild not found.")
            return

        channel = discord.utils.get(guild.channels, name="venting")
        if channel is None:
            await ctx.send("Target channel not found.")
            return

        await channel.send(f"Vent from {ctx.author.name}: {message}")
        await ctx.send("Message vented successfully!")

def setup(bot):
    bot.add_cog(VentCog(bot))
