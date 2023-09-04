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
            description=f"Support the @valor_bound by donating!\n[Click here to donate]({donation_link})",
            color=discord.Color.green()
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def slashdonate(self, ctx):
        # Replace 'YOUR_DONATION_LINK' with your actual donation link
        donation_link = 'https://cash.app/$taintedvalor'

        embed = discord.Embed(
            title="Donate",
            description=f"Support the @valor_bound by donating!\n[Click here to donate]({donation_link})",
            color=discord.Color.green()
        )

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(DonationCog(bot))
