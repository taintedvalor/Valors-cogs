import discord
from redbot.core import commands, Config

class BountyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=892347981)  # Change identifier to a unique value
        self.config.register_guild(bounties={})

    @commands.command()
    async def bountyboard(self, ctx):
        """Displays the current bounties on the bounty board."""
        bounties = await self.config.guild(ctx.guild).bounties()
        if not bounties:
            await ctx.send("No bounties currently available.")
            return

        bounty_list = ""
        for bounty, status in bounties.items():
            emoji = "✅" if status else "⌛"
            bounty_list += f"{emoji} {bounty}\n"

        embed = discord.Embed(title="Bounty Board", description=bounty_list, color=discord.Color.blurple())
        await ctx.send(embed=embed)

    @commands.command()
    async def acceptbounty(self, ctx, *, bounty_name):
        """Accepts a bounty and sends a direct message to the requester."""
        bounties = await self.config.guild(ctx.guild).bounties()
        if bounty_name in bounties and not bounties[bounty_name]:
            # Set the bounty as pending
            bounties[bounty_name] = True
            await self.config.guild(ctx.guild).bounties.set(bounties)

            # Send a DM to the requester
            requester_id = bounties[bounty_name]
            requester = await self.bot.fetch_user(requester_id)
            await requester.send(f"Your bounty '{bounty_name}' has been accepted by {ctx.author.name}.")

            await ctx.send(f"{ctx.author.mention} has accepted the bounty '{bounty_name}'.")
        else:
            await ctx.send("Invalid bounty or it has already been accepted.")

    @commands.command()
    async def completebounty(self, ctx, *, bounty_name):
        """Marks a bounty as completed and removes it from the bounty board."""
        bounties = await self.config.guild(ctx.guild).bounties()
        if bounty_name in bounties and bounties[bounty_name]:
            # Remove the bounty from the board
            del bounties[bounty_name]
            await self.config.guild(ctx.guild).bounties.set(bounties)

            await ctx.send(f"The bounty '{bounty_name}' has been marked as completed.")
        else:
            await ctx.send("Invalid bounty or it has not been accepted yet.")

    @commands.command()
    async def addbounty(self, ctx, *, bounty_name):
        """Adds a new bounty to the bounty board."""
        bounties = await self.config.guild(ctx.guild).bounties()
        if bounty_name not in bounties:
            # Add the bounty to the board
            bounties[bounty_name] = False
            await self.config.guild(ctx.guild).bounties.set(bounties)

            await ctx.send(f"The bounty '{bounty_name}' has been added to the bounty board.")
        else:
            await ctx.send("This bounty already exists.")

def setup(bot):
    bot.add_cog(BountyCog(bot))
