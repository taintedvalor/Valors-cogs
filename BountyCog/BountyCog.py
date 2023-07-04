import discord
from redbot.core import commands, Config

class BountyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=892347981)  # Change identifier to a unique value
        self.config.register_guild(bounty_channel=None, bounties={})

    @commands.command()
    async def bountyboard(self, ctx):
        """Displays the current bounties on the bounty board."""
        bounties = await self.config.guild(ctx.guild).bounties()
        if not bounties:
            await ctx.send("No bounties currently available.")
            return

        bounty_list = ""
        for bounty, data in bounties.items():
            status = data["status"]
            description = data["description"]
            emoji = "✅" if status else "⌛"
            bounty_list += f"{emoji} {bounty} - {description}\n"

        embed = discord.Embed(title="Bounty Board", description=bounty_list, color=discord.Color.blurple())
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.admin_or_permissions(manage_guild=True)
    async def createbountychannel(self, ctx, channel: discord.TextChannel):
        """Creates a bounty channel to display the dynamic bounty board."""
        await self.config.guild(ctx.guild).bounty_channel.set(channel.id)
        await channel.purge()
        await self.update_bounty_embed(ctx.guild)

    async def update_bounty_embed(self, guild):
        bounties = await self.config.guild(guild).bounties()
        channel_id = await self.config.guild(guild).bounty_channel()
        if not channel_id:
            return

        channel = guild.get_channel(channel_id)
        if not channel:
            return

        messages = await channel.history().flatten()
        await channel.purge()

        bounty_list = ""
        for bounty, data in bounties.items():
            status = data["status"]
            description = data["description"]
            emoji = "✅" if status else "⌛"
            bounty_list += f"{emoji} {bounty} - {description}\n"

        embed = discord.Embed(title="Bounty Board", description=bounty_list, color=discord.Color.blurple())
        message = await channel.send(embed=embed)

        if messages:
            try:
                for message in messages:
                    await message.delete()
            except discord.Forbidden:
                pass

    @commands.command()
    async def acceptbounty(self, ctx, *, bounty_name):
        """Accepts a bounty and sends a direct message to the requester."""
        bounties = await self.config.guild(ctx.guild).bounties()
        if bounty_name in bounties and not bounties[bounty_name]["status"]:
            # Set the bounty as pending
            bounties[bounty_name]["status"] = True
            await self.config.guild(ctx.guild).bounties.set(bounties)

            # Send a DM to the requester
            requester_id = bounties[bounty_name]["requester_id"]
            requester = await self.bot.fetch_user(requester_id)
            await requester.send(f"Your bounty '{bounty_name}' has been accepted by {ctx.author.name}.")

            await ctx.send(f"{ctx.author.mention} has accepted the bounty '{bounty_name}'.")
            await self.update_bounty_embed(ctx.guild)
        else:
            await ctx.send("Invalid bounty or it has already been accepted.")

    @commands.command()
    async def completebounty(self, ctx, *, bounty_name):
        """Marks a bounty as completed and removes it from the bounty board."""
        bounties = await self.config.guild(ctx.guild).bounties()
        if bounty_name in bounties and bounties[bounty_name]["status"]:
            # Remove the bounty from the board
            del bounties[bounty_name]
            await self.config.guild(ctx.guild).bounties.set(bounties)

            await ctx.send(f"The bounty '{bounty_name}' has been marked as completed.")
            await self.update_bounty_embed(ctx.guild)
        else:
            await ctx.send("Invalid bounty or it has not been accepted yet.")

    @commands.command()
    async def addbounty(self, ctx, bounty_name, *, description):
        """Adds a new bounty to the bounty board."""
        bounties = await self.config.guild(ctx.guild).bounties()
        if bounty_name not in bounties:
            # Add the bounty to the board
            bounties[bounty_name] = {
                "status": False,
                "description": description,
                "requester_id": ctx.author.id
            }
            await self.config.guild(ctx.guild).bounties.set(bounties)

            await ctx.send(f"The bounty '{bounty_name}' has been added to the bounty board.")
            await self.update_bounty_embed(ctx.guild)
        else:
            await ctx.send("This bounty already exists.")

def setup(bot):
    bot.add_cog(BountyCog(bot))

