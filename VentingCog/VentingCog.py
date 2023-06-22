from redbot.core import commands, Config
from redbot.core.i18n import cog_i18n, Translator
from typing import Optional

import discord

_ = Translator("Ventingcog", __file__)

@cog_i18n(_)
class Ventingcog(commands.Cog):
    __version__ = "1.0.0"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)
        self.config.register_global(server_channel_mapping={})

    def format_help_for_context(self, ctx):
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        # No user data stored
        return

    @commands.command()
    async def vent(self, ctx, server_name: str, *, text: Optional[str]):
        """Submit an anonymous vent to the designated venting room in a server."""
        mapping = await self.config.server_channel_mapping()
        server_id = mapping.get(server_name.lower())
        if server_id is None:
            await ctx.send(_("The specified server is not configured for venting."))
            return

        server = self.bot.get_guild(server_id)
        if server is None:
            await ctx.send(_("The specified server is not found."))
            return

        channel = self.get_venting_channel(server)
        if channel is None:
            await ctx.send(_("The venting channel is not configured for the specified server."))
            return

        anonymous_name = _("Anonymous")
        anonymous_avatar = self.bot.user.default_avatar_url

        embed = discord.Embed(
            title=_("New Anonymous Vent"),
            description=text,
            color=discord.Color.dark_grey()
        )
        embed.set_author(name=anonymous_name, icon_url=anonymous_avatar)

        await channel.send(embed=embed)
        await ctx.send(_("Your vent has been posted anonymously in {server}'s venting channel.").format(server=server.name))

    @commands.command()
    async def configureventing(self, ctx, server_name: str, channel: discord.TextChannel):
        """Configure a server's venting channel."""
        mapping = await self.config.server_channel_mapping()
        server_id = mapping.get(server_name.lower())
        if server_id is None:
            mapping[server_name.lower()] = channel.guild.id
            await self.config.server_channel_mapping.set(mapping)
            await ctx.send(_("Venting channel configured for {server}.").format(server=server_name))
        else:
            await ctx.send(_("Venting channel is already configured for {server}.").format(server=server_name))

    def get_venting_channel(self, server: discord.Guild) -> Optional[discord.TextChannel]:
        mapping = self.config.server_channel_mapping()
        server_id = mapping.get(server.name.lower())
        if server_id is not None:
            return server.get_channel(server_id)
        return None
