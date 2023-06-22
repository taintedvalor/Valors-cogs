import discord
from discord.ext import commands

class VentCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def vent(self, ctx, *, message):
        guild_id = 1034864936997900428  # Replace with your target guild ID
        guild = self.bot.get_guild(guild_id)
        if guild is None:
            await ctx.send("Target guild not found.")
            return

        channel_name = "venting"
        channel = discord.utils.get(guild.channels, name=channel_name)
        if channel is None:
            await ctx.send("Target channel not found.")
            return

        await channel.send(f"Vent from {ctx.author.name}: {message}")
        await ctx.send("Message vented successfully!")

def setup(bot):
    bot.add_cog(VentCog(bot))
