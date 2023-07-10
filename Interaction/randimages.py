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
    async def waifu(self, ctx: commands.MemberConverter):
        """summon a waifu."""

        await self._send_other_msg(
            ctx,
            name=_(f"{ctx.author.name} has summoned a waifu!"),
            emoji="",
            source="nekos.life",
            img_url="https://nekos.life/api/v2/img/waifu",
            img_arg="url",
            facts=False,

        )
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command()
    async def smug(self, ctx: commands.MemberConverter):
        """Express smugness."""
        await self._send_other_msg(
            ctx,
            name=f"{ctx.author.name} is smug!",
            emoji="😏",
            source="nekos.life",
            img_url="https://nekos.life/api/v2/img/smug",
            img_arg="url",
            facts=False,
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command()
    async def tickle(self, ctx, user: commands.MemberConverter):
        """Tickle someone."""
        await self._send_other_msg(
            ctx,
            name=f"{ctx.author.name} tickles {user.name}!",
            emoji="😄",
            source="nekos.life",
            img_url="https://nekos.life/api/v2/img/tickle",
            img_arg="url",
            facts=False,
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command()
    async def pat(self, ctx, user: commands.MemberConverter):
        """Pat someone."""
        await self._send_other_msg(
            ctx,
            name=f"{ctx.author.name} pats {user.name}!",
            emoji="👋",
            source="nekos.life",
            img_url="https://nekos.life/api/v2/img/pat",
            img_arg="url",
            facts=False,
        )
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command()
    async def punch(self, ctx, user: commands.MemberConverter):
        """Punch someone."""
        await self._send_other_msg(
            ctx,
            name=f"{ctx.author.name} pats {user.name}!",
            emoji="👋",
            source="nekos.life",
            img_url="https://nekos.life/api/v2/img/punch",
            img_arg="url",
            facts=False,
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command()
    async def rule34(self, ctx: commands.Context):
        """Send a random photography from random subreddits."""

        await self._send_reddit_msg(
            ctx,
            name=_("rule34"),
            emoji="\N{CAMERA WITH FLASH}",
            sub=sub.RULE34,
            details=True,
        )


    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command()
    async def fuck(self, ctx, user: commands.MemberConverter):
        """fuck someone."""

        await self._send_reddit_msg(
            ctx,
            name=f"{ctx.author.name} tickles {user.name}!",
            emoji="\N{CAMERA WITH FLASH}",
            sub=sub.FUCK,
            details=False,
        )
