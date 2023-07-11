from logging import LoggerAdapter
from typing import Final, Any

import aiohttp
import discord
from redbot.core.bot import Red
from redbot.core import checks, commands
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils.chat_formatting import box
from red_commons.logging import RedTraceLogger, getLogger

from .rolecore import ACTIONS, ICON, NEKOS
from .core import Core
from . import constants as sub

_ = Translator("Image", __file__)


@cog_i18n(_)
class RandImages(Core):
    """Send random images (animals, art ...) from different APIs."""

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command()
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
        """Send a random rule34 image from random subreddits."""

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
        """Fuck someone."""

        await self._send_reddit_msg(
            ctx,
            name=f"{ctx.author.name} fucks {user.name}!",
            emoji="",
            sub=sub.FUCK,
            details=False,
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command()
    async def art(self, ctx: commands.Context):
        """Send art from random subreddits."""

        await self._send_reddit_msg(
            ctx, name=_("art image"), emoji="\N{ARTIST PALETTE}", sub=sub.ART, details=True
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command()
    async def birb(self, ctx: commands.Context):
        """Send a random birb image from alexflipnote API."""

        await self._send_other_msg(
            ctx,
            name=_("birb"),
            emoji="\N{BIRD}",
            source="alexflipnote API",
            img_url="https://api.alexflipnote.dev/birb",
            img_arg="file",
            facts=False,
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command(aliases=["cats"])
    async def cat(self, ctx: commands.Context):
        """Send a random cat image some-random-api.ml API."""

        await self._send_other_msg(
            ctx,
            name=_("cat"),
            emoji="\N{CAT FACE}",
            source="nekos.life",
            img_url="https://nekos.life/api/v2/img/meow",
            img_arg="url",
            facts=False,
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command(aliases=["catsfact"])
    async def catfact(self, ctx: commands.Context):
        """Send a random cat fact with a random cat image from some-random-api.ml API."""

        await self._send_other_msg(
            ctx,
            name=_("a cat fact with a random cat image"),
            emoji="\N{CAT FACE}",
            source="nekos.life",
            img_url="https://nekos.life/api/v2/img/meow",
            img_arg="url",
            facts_url="https://some-random-api.ml/facts/cat",
            facts_arg="fact",
            facts=True,
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command()
    async def coffee(self, ctx: commands.Context):
        """Send a random coffee image from alexflipnote API."""

        await self._send_other_msg(
            ctx,
            name=_("your coffee"),
            emoji="\N{HOT BEVERAGE}",
            source="alexflipnote API",
            img_url="https://coffee.alexflipnote.dev/random.json",
            img_arg="file",
            facts=False,
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command(aliases=["cuteness"])
    async def cute(self, ctx: commands.Context):
        """Send a random cute images from random subreddits."""

        await self._send_reddit_msg(
            ctx, name=_("a cute image"), emoji="❤️", sub=sub.CUTE, details=False
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command(aliases=["dogs"])
    async def dog(self, ctx: commands.Context):
        """Send a random dog image from random.dog API."""

        await self._send_other_msg(
            ctx,
            name=_("dog"),
            emoji="\N{DOG FACE}",
            source="random.dog",
            img_url="https://random.dog/woof.json",
            img_arg="url",
            facts=False,
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command(aliases=["dogsfact"])
    async def dogfact(self, ctx: commands.Context):
        """Send a random dog fact with a random dog image from some-random-api.ml API."""

        await self._send_other_msg(
            ctx,
            name=_("a dog fact with a random dog image"),
            emoji="\N{DOG FACE}",
            source="random.dog",
            img_url="https://random.dog/woof.json",
            img_arg="url",
            facts_url="https://some-random-api.ml/facts/dog",
            facts_arg="fact",
            facts=True,
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command()
    async def duck(self, ctx: commands.Context):
        """Send a random duck image from random subreddits."""

        await self._send_reddit_msg(
            ctx, name=_("a duck image"), emoji="\N{DUCK}", sub=sub.DUCKS, details=False
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command(aliases=["ferrets"])
    async def ferret(self, ctx: commands.Context):
        """Send a random ferrets images from random subreddits."""

        await self._send_reddit_msg(
            ctx, name=_("a ferret image"), emoji="❤️", sub=sub.FERRETS, details=False
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command(aliases=["foxes"])
    async def fox(self, ctx: commands.Context):
        """Send a random fox image from randomfox.ca API"""

        await self._send_other_msg(
            ctx,
            name=_("fox"),
            emoji="\N{FOX FACE}",
            source="randomfox.ca",
            img_url="https://randomfox.ca/floof",
            img_arg="image",
            facts=False,
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command(aliases=["pandas"])
    async def panda(self, ctx: commands.Context):
        """Send a random panda image from some-random-api.ml API."""

        await self._send_other_msg(
            ctx,
            name=_("panda"),
            emoji="\N{PANDA FACE}",
            source="some-random-api.ml",
            img_url="https://some-random-api.ml/img/panda",
            img_arg="link",
            facts=False,
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command()
    async def lizard(self, ctx: commands.Context):
        """Send a random lizard image from nekos.life API"""

        await self._send_other_msg(
            ctx,
            name=_("lizard"),
            emoji="\N{LIZARD}",
            source="nekos.life",
            img_url="https://nekos.life/api/lizard",
            img_arg="url",
            facts=False,
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command(aliases=["memes"])
    async def meme(self, ctx: commands.Context):
        """Send a random dank meme from random subreddits."""

        await self._send_reddit_msg(
            ctx, name=_("meme image"), emoji="\N{OK HAND SIGN}", sub=sub.MEMES, details=False
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command(aliases=["pandasfact"])
    async def pandafact(self, ctx: commands.Context):
        """Send a random panda fact with a random panda image from some-random-api.ml API."""

        await self._send_other_msg(
            ctx,
            name=_("a panda fact with a random panda image"),
            emoji="\N{PANDA FACE}",
            source="some-random-api.ml",
            img_url="https://some-random-api.ml/img/panda",
            img_arg="link",
            facts_url="https://some-random-api.ml/facts/panda",
            facts_arg="fact",
            facts=True,
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command(aliases=["pikachu"])
    async def pika(self, ctx: commands.Context):
        """Send a random Pikachu image or GIF from some-random-api.ml API."""

        await self._send_other_msg(
            ctx,
            name=_("Pikachu"),
            emoji="❤️",
            source="some-random-api.ml",
            img_url="https://some-random-api.ml/img/pikachu",
            img_arg="link",
            facts=False,
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command()
    async def shiba(self, ctx: commands.Context):
        """Send a random shiba image from shiba.online API."""

        await self._send_other_msg(
            ctx,
            name=_("shiba"),
            emoji="\N{DOG FACE}",
            source="shibe.online",
            img_url="http://shibe.online/api/shibes",
            img_arg=0,
            facts=False,
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command(aliases=["photography"])
    async def photo(self, ctx: commands.Context):
        """Send a random photography from random subreddits."""

        await self._send_reddit_msg(
            ctx,
            name=_("a photography"),
            emoji="\N{CAMERA WITH FLASH}",
            sub=sub.PHOTOS,
            details=True,
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command(aliases=["subr"])
    @commands.max_concurrency(1, commands.BucketType.user, wait=False)
    async def subreddit(self, ctx: commands.Context, *, subreddit: str):
        """Send a random image from a chosen subreddit."""
        if subreddit in ["friends", "mod"]:
            return await ctx.send("This isn't a valid subreddit.")

        await self._send_reddit_msg(
            ctx,
            name=_("random image"),
            emoji="\N{FRAME WITH PICTURE}",
            sub=[str(subreddit)],
            details=True,
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command(aliases=["wallp"])
    async def wallpaper(self, ctx: commands.Context):
        """Send a random wallpaper image from random subreddits."""

        await self._send_reddit_msg(
            ctx,
            name=_("a wallpaper"),
            emoji="\N{FRAME WITH PICTURE}",
            sub=sub.WALLPAPERS,
            details=True,
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command(aliases=["wack"])
    async def bonk(self, ctx, user: commands.MemberConverter):
        """bonk someone."""

        await self._send_reddit_msg(
            ctx,
            name=f"{ctx.author.name} bonks {user.name}!",
            emoji="",
            sub=sub.BONK,
            details=False,
        )


log: RedTraceLogger = getLogger("red.maxcogs.roleplaycog")

    def __init__(self, bot: Red) -> None:
        self.bot: Red = bot
        self.session: aiohttp.ClientSession = aiohttp.ClientSession()

        self.log: LoggerAdapter[RedTraceLogger] = LoggerAdapter(log, {"version": self.__version__})

    async def cog_unload(self):
        await self.session.close()

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nAuthor: {self.__author__}\nCog Version: {self.__version__}\nDocs: {self.__docs__}"

    async def red_delete_data_for_user(self, **kwargs: Any) -> None:
        """Nothing to delete."""
        return

    async def embedgen(self, ctx: commands.Context, member: discord.Member, action: str) -> None:
        async with self.session.get(NEKOS + action) as response:
            if response.status != 200:
                await ctx.send(
                    "Something went wrong while trying to contact API."
                )
                return
            data = await response.json()

        action_fmt = ACTIONS.get(action, action)
        anime_name = data["results"][0]["anime_name"]
        emb = discord.Embed(
            colour=await ctx.embed_color(),
            description=(
                f"{ctx.author.mention} {action_fmt} {f'{member.mention}' if member else 'themselves!'}\n"
            ),
        )
        emb.set_footer(
            text=f"Powered by nekos.best\nAnime Name: {anime_name}", icon_url=ICON
        )
        emb.set_image(url=data["results"][0]["url"])
        await ctx.send(embed=emb)

    @commands.bot_has_permissions(embed_links=True)
    @commands.command(name="rpcversion", hidden=True)
    async def roleplaycog_version(self, ctx: commands.Context) -> None:
        """Shows the version of the cog."""
        version = self.__version__
        author = self.__author__
        embed = discord.Embed(
            title="Cog Information",
            description=box(
                f"{'Cog Author':<11}: {author}\n{'Cog Version':<10}: {version}",
                lang="yaml",
            ),
            color=await ctx.embed_color(),
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def baka(self, ctx: commands.Context, member: discord.Member) -> None:
        """Baka baka baka!"""
        await self.embedgen(ctx, member, "baka")

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def cry(self, ctx: commands.Context, member: discord.Member) -> None:
        """Cry!"""
        await self.embedgen(ctx, member, "cry")

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def cuddle(self, ctx: commands.Context, member: discord.Member) -> None:
        """Cuddle a user!"""
        await self.embedgen(ctx, member, "cuddle")

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def dance(self, ctx: commands.Context, member: discord.Member) -> None:
        """Dance!"""
        await self.embedgen(ctx, member, "dance")

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def feed(self, ctx: commands.Context, member: discord.Member) -> None:
        """Feeds a user!"""
        await self.embedgen(ctx, member, "feed")

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def hugs(self, ctx: commands.Context, member: discord.Member) -> None:
        """Hugs a user!"""
        await self.embedgen(ctx, member, "hug")

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def kiss(self, ctx: commands.Context, member: discord.Member) -> None:
        """Kiss a user!"""
        await self.embedgen(ctx, member, "kiss")

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def laugh(self, ctx: commands.Context, member: discord.Member) -> None:
        """laugh!"""
        await self.embedgen(ctx, member, "laugh")

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def pat(self, ctx: commands.Context, member: discord.Member) -> None:
        """Pats a user!"""
        await self.embedgen(ctx, member, "pat")

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def pokes(self, ctx: commands.Context, member: discord.Member) -> None:
        # Due to conflict with pokecord cog, it has to be pokes.
        # Feel free to use alias cog if you want poke only.
        """Pokes at a user!"""
        await self.embedgen(ctx, member, "poke")

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def slap(self, ctx: commands.Context, member: discord.Member) -> None:
        """Slap a user!"""
        await self.embedgen(ctx, member, "slap")

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def smile(self, ctx: commands.Context, member: discord.Member) -> None:
        """Smile!"""
        await self.embedgen(ctx, member, "smile")

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def smug(self, ctx: commands.Context, member: discord.Member) -> None:
        """Smugs at someone!"""
        await self.embedgen(ctx, member, "smug")

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def tickle(self, ctx: commands.Context, member: discord.Member) -> None:
        """Tickle a user!"""
        await self.embedgen(ctx, member, "tickle")

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def wave(self, ctx: commands.Context, member: discord.Member) -> None:
        """Waves!"""
        await self.embedgen(ctx, member, "wave")

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def bite(self, ctx: commands.Context, member: discord.Member) -> None:
        """Bite a user!"""
        await self.embedgen(ctx, member, "bite")

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def blush(self, ctx: commands.Context, member: discord.Member) -> None:
        """blushes!"""
        await self.embedgen(ctx, member, "blush")

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def bored(self, ctx: commands.Context, member: discord.Member) -> None:
        """You're bored!"""
        await self.embedgen(ctx, member, "bored")

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def facepalm(self, ctx: commands.Context, member: discord.Member) -> None:
        """Facepalm at a user!"""
        await self.embedgen(ctx, member, "facepalm")

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def happy(self, ctx: commands.Context, member: discord.Member) -> None:
        """happiness with a user!"""
        await self.embedgen(ctx, member, "happy")

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def highfive(self, ctx: commands.Context, member: discord.Member) -> None:
        """highfive a user!"""
        await self.embedgen(ctx, member, "highfive")

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def pout(self, ctx: commands.Context, member: discord.Member) -> None:
        """Pout a user!"""
        await self.embedgen(ctx, member, "pout")

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def shrug(self, ctx: commands.Context, member: discord.Member) -> None:
        """Shrugs a user!"""
        await self.embedgen(ctx, member, "shrug")

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def sleep(self, ctx: commands.Context, member: discord.Member) -> None:
        """Sleep zzzz!"""
        await self.embedgen(ctx, member, "sleep")

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def stare(self, ctx: commands.Context, member: discord.Member) -> None:
        """Stares at a user!"""
        await self.embedgen(ctx, member, "stare")

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def think(self, ctx: commands.Context, member: discord.Member) -> None:
        """Thinking!"""
        await self.embedgen(ctx, member, "think")

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def thumbsup(self, ctx: commands.Context, member: discord.Member) -> None:
        """thumbsup!"""
        await self.embedgen(ctx, member, "thumbsup")

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def wink(self, ctx: commands.Context, member: discord.Member) -> None:
        """Winks at a user!"""
        await self.embedgen(ctx, member, "wink")

    @commands.command(aliases=["handholding"])
    @commands.bot_has_permissions(embed_links=True)
    async def handhold(self, ctx: commands.Context, member: discord.Member) -> None:
        """handhold a user!"""
        await self.embedgen(ctx, member, "handhold")

    @commands.command(aliases=["vkicks"])
    @commands.bot_has_permissions(embed_links=True)
    async def vkick(self, ctx: commands.Context, member: discord.Member) -> None:
        """kick a user!"""
        await self.embedgen(ctx, member, "kick")

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def punch(self, ctx: commands.Context, member: discord.Member) -> None:
        """punch a user!"""
        await self.embedgen(ctx, member, "punch")

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def shoot(self, ctx: commands.Context, member: discord.Member) -> None:
        """shoot a user!"""
        await self.embedgen(ctx, member, "shoot")

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def yeet(self, ctx: commands.Context, member: discord.Member) -> None:
        """yeet a user far far away."""
        await self.embedgen(ctx, member, "yeet")

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def nod(self, ctx: commands.Context, member: discord.Member) -> None:
        """nods a user far far away."""
        await self.embedgen(ctx, member, "nod")

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def nope(self, ctx: commands.Context, member: discord.Member) -> None:
        """nope a user far far away."""
        await self.embedgen(ctx, member, "nope")

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def nom(self, ctx: commands.Context, member: discord.Member) -> None:
        """nom nom a user far far away."""
        await self.embedgen(ctx, member, "nom")
