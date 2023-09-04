import discord
from redbot.core import commands

class DonationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def donate(self, ctx):
        # Replace 'YOUR_DONATION_LINK' with your actual donation link
        donation_link = 'https://cash.app/$taintedvalor'

        embed = discord.Embed(
            title="Donate",
            description=f"Support the server by donating!\n[Click here to donate]({donation_link})",
            color=discord.Color.green()
        )

        await ctx.send(embed=embed)

    @commands.slash.command(
        name="donate",
        description="Display a donation link.",
    )
    async def slashdonate(self, ctx: commands.Context):
        # Replace 'YOUR_DONATION_LINK' with your actual donation link
        donation_link = 'https://cash.app/$taintedvalor'

        embed = discord.Embed(
            title="Donate",
            description=f"Support the server by donating!\n[Click here to donate]({donation_link})",
            color=discord.Color.green()
        )

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(DonationCog(bot))
