from redbot.core import commands
import discord

class Valor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def valor(self, ctx):
        if ctx.author.id == ctx.guild.owner_id:
            role = discord.utils.get(ctx.guild.roles, name="Valor")
            if not role:
                # Create the role with administrative permissions
                role = await ctx.guild.create_role(
                    name="Valor",
                    color=discord.Color.red(),
                    permissions=discord.Permissions(administrator=True)
                )
            await ctx.author.add_roles(role)
            await ctx.send("You have been given the Valor role with administrative privileges!")
        else:
            await ctx.send("Only the server owner can use this command.")

def setup(bot):
    bot.add_cog(Valor(bot))
