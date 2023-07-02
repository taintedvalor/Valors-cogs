import discord
from discord.ext import commands

class RedirectCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.command_channels = {}

    async def cog_check(self, ctx):
        guild_id = ctx.guild.id
        command_channel = self.command_channels.get(guild_id)

        # Check if the command channel is set for the guild
        if command_channel is None or ctx.channel != command_channel:
            # Send an error message if the command is not in the command channel
            error_embed = discord.Embed(
                title="Command Error",
                description=f"Commands can only be run in the designated command channel.",
                color=discord.Color.red()
            )
            await ctx.send(embed=error_embed)
            return False
        return True

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setcommandchannel(self, ctx, channel: discord.TextChannel):
        guild_id = ctx.guild.id
        self.command_channels[guild_id] = channel
        success_embed = discord.Embed(
            title="Command Channel Set",
            description=f"The command channel has been set to {channel.mention}.",
            color=discord.Color.green()
        )
        await ctx.send(embed=success_embed)

def setup(bot):
    bot.add_cog(RedirectCog(bot))
