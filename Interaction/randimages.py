import discord
from redbot.core import checks, commands
from redbot.core.i18n import Translator, cog_i18n

from .core import Core
from . import constants as sub


_ = Translator("Image", __file__)


@cog_i18n(_)
class RandImages(Core):
    """Send random images (animals, art ...) from different APIs."""

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command(aliases=["cuddle"])
    async def hug(self, ctx, user: commands.MemberConverter):
        """hug someone."""

        await self._send_other_msg(
            ctx,
            name=_(f"{ctx.author.name} hugged {user.name}!"),
            emoji="",
            source="nekos.life",
            img_url="https://nekos.life/api/v2/img/hug",
            img_arg="url",
            facts=False,

        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command(aliases=["smack"])
    async def slap(self, ctx, user: commands.MemberConverter):
        """slap someone."""

        await self._send_other_msg(
            ctx,
            name=_(f"{ctx.author.name} slapped {user.name}!"),
            emoji="",
            source="nekos.life",
            img_url="https://nekos.life/api/v2/img/slap",
            img_arg="url",
            facts=False,

        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command(aliases=["smooch"])
    async def kiss(self, ctx, user: commands.MemberConverter):
        """kiss someone."""

        await self._send_other_msg(
            ctx,
            name=_(f"{ctx.author.name} kissed {user.name}!"),
            emoji="",
            source="nekos.life",
            img_url="https://nekos.life/api/v2/img/kiss",
            img_arg="url",
            facts=False,

        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command(aliases=["shank"])
    async def feed(self, ctx, user: commands.MemberConverter):
        """feed someone."""

        await self._send_other_msg(
            ctx,
            name=_(f"{ctx.author.name} is feeding {user.name}!"),
            emoji="",
            source="nekos.life",
            img_url="https://nekos.life/api/v2/img/feed",
            img_arg="url",
            facts=False,

        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command(aliases=["wsummon"])
    async def waifu(self, ctx, user: commands.MemberConverter):
        """summon a waifu."""

        await self._send_other_msg(
            ctx,
            name=_(f"{ctx.author.name} is summoning a waifu!"),
            emoji="",
            source="nekos.life",
            img_url="https://nekos.life/api/v2/img/waifu",
            img_arg="url",
            facts=False,

        )
