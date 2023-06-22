import logging
import asyncio
from typing import List, Literal
from datetime import timedelta
from copy import copy
import contextlib
import discord

from redbot.core import Config, commands
from redbot.core.utils import AsyncIter
from redbot.core.utils.chat_formatting import pagify, box
from redbot.core.utils.antispam import AntiSpam
from redbot.core.bot import Red
from redbot.core.i18n import Translator, cog_i18n, set_contextual_locales_from_guild
from redbot.core.utils.predicates import MessagePredicate
from redbot.core.utils.tunnel import Tunnel


_ = Translator("Venting", __file__)

log = logging.getLogger("red.venting")


@cog_i18n(_)
class Venting(commands.Cog):
    """An anonymous venting cog for users to express their feelings."""

    default_guild_settings = {"output_channel": None, "active": False, "next_ticket": 1}

    default_vent = {"message": ""}

    # This can be made configurable later if it
    # becomes an issue.
    # Intervals should be a list of tuples in the form
    # (period: timedelta, max_frequency: int)
    # see redbot/core/utils/antispam.py for more details

    intervals = [
        (timedelta(seconds=5), 1),
        (timedelta(minutes=5), 3),
        (timedelta(hours=1), 10),
        (timedelta(days=1), 24),
    ]

    def __init__(self, bot: Red):
        super().__init__()
        self.bot = bot
        self.config = Config.get_conf(self, 78631113035100160, force_registration=True)
        self.config.register_guild(**self.default_guild_settings)
        self.config.init_custom("VENT", 2)
        self.config.register_custom("VENT", **self.default_vent)
        self.antispam = {}
        self.user_cache = []
        self.tunnel_store = {}

    async def red_delete_data_for_user(
        self,
        *,
        requester: Literal["discord_deleted_user", "owner", "user", "user_strict"],
        user_id: int,
    ):
        if requester != "discord_deleted_user":
            return

        all_vents = await self.config.custom("VENT").all()

        steps = 0
        paths = []

        for guild_id_str, vent in all_vents.items():
            steps += 1
            if not steps % 100:
                await asyncio.sleep(0)  # yield context

            if vent.get("user_id", 0) == user_id:
                paths.append(guild_id_str)

        async with self.config.custom("VENT").all() as all_vents:
            async for guild_id_str in AsyncIter(paths, steps=100):
                v = all_vents[guild_id_str]
                v["user_id"] = 0xDE1
                v["message"] = "[VENT DELETED DUE TO DISCORD REQUEST]"

    async def internal_filter(self, m: discord.Member, mod=False, perms=None):
        if perms is not None and m.guild_permissions >= perms:
            return True
        if mod and await self.bot.is_mod(m):
            return True
        if await self.bot.is_owner(m):
            return True

    async def discover_guild(
        self,
        author: discord.User,
        *,
        mod: bool = False,
        permissions: Union[discord.Permissions, dict] = None,
        prompt: str = "",
    ):
        guilds = self.bot.guilds
        with contextlib.suppress(AttributeError):
            guilds = await self.bot.fetch_guilds().flatten()

        if permissions is not None and not isinstance(permissions, discord.Permissions):
            perms = discord.Permissions(**permissions)
        else:
            perms = permissions

        message = ""

        if author in self.user_cache:
            guilds = await asyncio.gather(*[self.bot.fetch_guild(g) for g in self.user_cache])
        else:
            for guild in guilds:
                async with self.config.guild(guild).output_channel() as channel:
                    if channel is None:
                        continue
                    channel = self.bot.get_channel(channel)
                    if not isinstance(channel, discord.TextChannel):
                        continue
                    perms = await self.internal_filter(author, mod=mod, perms=perms)
                    if perms:
                        self.user_cache.append(guild.id)
                        message += f"ID: {guild.id} | Name: {guild.name}\n"

        if not message:
            return None

        if len(message) > 1500:
            message = message[: message.rfind("\n", 0, 1500)]

        await author.send(f"{prompt}```http\n{message}```")

    async def send_vent(
        self,
        guild: discord.Guild,
        author: discord.User,
        msg: str,
        message=None,
        *,
        attachment: discord.Attachment = None,
    ):
        next_ticket = await self.config.guild(guild).next_ticket()
        await self.config.guild(guild).next_ticket.set(next_ticket + 1)
        vent_settings = await self.config.custom("VENT", next_ticket).all()

        channel_id = await self.config.guild(guild).output_channel()
        channel = guild.get_channel(channel_id)
        if channel is None:
            return

        vent_settings["user_id"] = author.id
        vent_settings["message"] = msg

        if attachment:
            vent_settings["attachments"] = vent_settings.get("attachments", [])
            vent_settings["attachments"].append(str(attachment.url))

        vent_settings["guild_name"] = str(guild)
        vent_settings["guild_id"] = guild.id
        vent_settings["channel_id"] = channel.id

        async with self.config.custom("VENT", next_ticket).all() as new_settings:
            new_settings.update(vent_settings)

        tickets = len(await self.config.custom("VENT").all())

        if tickets == 1:
            to_singular = _("There is 1 open vent ticket.")
            await channel.send(f"{to_singular} {author.mention}")
        else:
            to_plural = _("There are {num_tickets} open vent tickets.")
            await channel.send(f"{to_plural} {author.mention}")

        if message:
            try:
                await message.delete()
            except (discord.NotFound, discord.Forbidden):
                pass

    @commands.command(name="vent", aliases=["anonymousvent", "avent"])
    @commands.guild_only()
    async def anonymous_vent(self, ctx: commands.Context, *, message: str):
        """
        Anonymously vent your feelings.

        The message you provide will be sent to the configured vent output channel,
        allowing you to express your feelings anonymously. Staff members who have
        access to the vent output channel will be able to read and respond to your vent.

        Note: Staff members may still be able to identify the user based on the context
        or specific details mentioned in the vent message.
        """
        if not await self.config.guild(ctx.guild).active():
            return await ctx.send(_("Venting is not currently enabled in this server."))

        member = ctx.author
        if ctx.message.attachments:
            attachment = ctx.message.attachments[0]
        else:
            attachment = None

        if member.id in self.antispam:
            if self.antispam[member.id].spammy:
                return
            self.antispam[member.id].stamp()
        else:
            self.antispam[member.id] = AntiSpam(self.intervals)

        can_send = self.antispam[member.id].spammy

        if can_send:
            channel_id = await self.config.guild(ctx.guild).output_channel()
            channel = ctx.guild.get_channel(channel_id)
            if channel is None:
                return

            can_send = await self.internal_filter(member)
            if not can_send:
                return await ctx.send(
                    _("You are not authorized to send vents in this server.")
                )

        try:
            await ctx.message.delete()
        except (discord.NotFound, discord.Forbidden):
            pass

        await self.send_vent(ctx.guild, member, message, ctx.message, attachment=attachment)
        if can_send:
            await ctx.send(_("Your vent has been sent."), delete_after=5)

    @commands.command(name="ventchannel", aliases=["ventoutputchannel", "voc"])
    @commands.guild_only()
    @commands.mod_or_permissions(manage_channels=True)
    async def set_vent_channel(
        self, ctx: commands.Context, channel: discord.TextChannel = None
    ):
        """
        Set the channel for vent messages to be sent.

        By default, vent messages will be sent to the current output channel.
        If you provide a channel mention or ID, vent messages will be sent to that channel.
        Use this command without a channel mention or ID to reset to the current channel.
        """
        if channel is None:
            channel = ctx.channel

        await self.config.guild(ctx.guild).output_channel.set(channel.id)
        await ctx.send(_("The vent output channel has been set to {channel}.").format(channel=channel.mention))

    @commands.command(name="venttoggle", aliases=["ventactive"])
    @commands.guild_only()
    @commands.mod_or_permissions(manage_channels=True)
    async def toggle_venting(self, ctx: commands.Context):
        """Toggle venting in the server."""
        active = await self.config.guild(ctx.guild).active()
        await self.config.guild(ctx.guild).active.set(not active)

        if active:
            await ctx.send(_("Venting has been disabled in this server."))
        else:
            await ctx.send(_("Venting has been enabled in this server."))

    @commands.command(name="ventlist", aliases=["venttickets", "avlist"])
    @commands.guild_only()
    @commands.mod_or_permissions(manage_channels=True)
    async def list_vents(self, ctx: commands.Context, page: int = 1):
        """List all open vent tickets."""
        vents = await self.config.custom("VENT").all()
        if not vents:
            return await ctx.send(_("There are no open vent tickets."))

        paged_vents = list(pagify("\n".join([f"**Ticket #{k}** - {v['guild_name']} - {v['message']}" for k, v in vents.items()]), page_length=10))
        if not paged_vents:
            return await ctx.send(_("Invalid page number."))

        total_pages = len(paged_vents)
        page = max(1, min(page, total_pages))
        message = f"**{total_pages}** {_(total_pages):page}:\n{paged_vents[page - 1]}"

        embed = discord.Embed(
            title=_("Open Vent Tickets"),
            description=box(message),
            color=await ctx.embed_colour(),
        )
        embed.set_footer(text=_("Page {page}/{total_pages}").format(page=page, total_pages=total_pages))

        await ctx.send(embed=embed)

    @commands.command(name="ventreply", aliases=["avreply"])
    @commands.guild_only()
    @commands.mod_or_permissions(manage_channels=True)
    async def reply_to_vent(self, ctx: commands.Context, ticket_number: int, *, reply: str):
        """Reply to a vent ticket."""
        vents = await self.config.custom("VENT").all()
        if ticket_number not in vents:
            return await ctx.send(_("Invalid ticket number."))

        vent = vents[ticket_number]
        guild = ctx.bot.get_guild(vent["guild_id"])
        if guild is None:
            return await ctx.send(_("The guild for this ticket no longer exists."))

        channel = guild.get_channel(vent["channel_id"])
        if channel is None:
            return await ctx.send(_("The channel for this ticket no longer exists."))

        member = guild.get_member(vent["user_id"])
        if member is None:
            return await ctx.send(_("The user for this ticket no longer exists."))

        try:
            await channel.send(
                _("**Staff Reply** - Ticket #{ticket_number}\n\n{reply}")
                .format(ticket_number=ticket_number, reply=reply)
            )
            await ctx.send(_("Your reply has been sent."))
        except discord.Forbidden:
            await ctx.send(_("I don't have permissions to send messages in that channel."))

    @commands.command(name="ventclose", aliases=["avclose"])
    @commands.guild_only()
    @commands.mod_or_permissions(manage_channels=True)
    async def close_vent(self, ctx: commands.Context, ticket_number: int):
        """Close a vent ticket."""
        vents = await self.config.custom("VENT").all()
        if ticket_number not in vents:
            return await ctx.send(_("Invalid ticket number."))

        vent = vents[ticket_number]
        guild = ctx.bot.get_guild(vent["guild_id"])
        if guild is None:
            return await ctx.send(_("The guild for this ticket no longer exists."))

        try:
            await self.config.custom("VENT", ticket_number).clear()
            await ctx.send(_("The vent ticket has been closed."))
        except Exception as e:
            log.exception("Failed to close vent ticket")
            await ctx.send(_("An error occurred while closing the vent ticket."))


async def setup(bot):
    cog = Venting(bot)
    await cog.initialize()
    bot.add_cog(cog)
