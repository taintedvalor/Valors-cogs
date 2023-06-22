import discord
from discord.ext import commands

class VentCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def vent(self, ctx, *, text):
        guild_id = YOUR_GUILD_ID  # Replace with the ID of your selected guild
        channel_name = 'venting'  # Name of the text channel in the guild

        # Fetch the target guild
        guild = self.bot.get_guild(guild_id)
        if guild is None:
            return await ctx.send("Invalid guild ID.")

        # Find the target text channel
        channel = discord.utils.get(guild.channels, name=channel_name, type=discord.ChannelType.text)
        if channel is None:
            return await ctx.send("Could not find the venting channel in the guild.")

        # Forward the message to the venting channel
        await channel.send(text)
        await ctx.send("Your message has been forwarded to the venting channel.")

def setup(bot):
    bot.add_cog(VentCog(bot))
