from redbot.core import commands, Config
import discord

class RedirectCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)  # Replace with a unique identifier
        default_guild_settings = {"command_channel": None}
        self.config.register_guild(**default_guild_settings)

    @commands.Cog.listener()
    async def cog_check(self, ctx):
        command_channel = await self.config.guild(ctx.guild).command_channel()
        if command_channel is None or ctx.channel.id == command_channel:
            return True
        else:
            error_embed = discord.Embed(
                title="Command Error",
                description=f"Commands can only be run in the designated command channel.",
                color=discord.Color.red()
            )
            await ctx.send(embed=error_embed)
            return False

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setcommandchannel(self, ctx, channel: discord.TextChannel):
        await self.config.guild(ctx.guild).command_channel.set(channel.id)
        success_embed = discord.Embed(
            title="Command Channel Set",
            description=f"The command channel has been set to {channel.mention}.",
            color=discord.Color.green()
        )
        await ctx.send(embed=success_embed)

def setup(bot):
    bot.add_cog(RedirectCog(bot))
