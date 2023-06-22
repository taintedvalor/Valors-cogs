import logging
import asyncio
from typing import List, Literal, Union
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
        permissions: Union[discord.Permissions, int] = None,
    ) -> List[discord.Guild]:
        """Discover guilds for venting in DMs"""
        guilds = [g for g in self.bot.guilds if await self.internal_filter(author, mod, permissions)]
        return guilds

    async def send_discoverable_guilds(
        self,
        ctx: commands.Context,
        guilds: List[discord.Guild],
        message: str = "Please select a guild from the following list:",
    ) -> discord.Guild:
        """Send a list of discoverable guilds and return the selected guild"""
        embed = discord.Embed(
            title="Available Guilds",
            description=message,
            colour=await ctx.embed_colour(),
        )
        for index, guild in enumerate(guilds, start=1):
            embed.add_field(
                name=f"Guild {index}",
                value=f"**Name**: {guild.name}\n**ID**: {guild.id}",
                inline=False,
            )

        embed.set_footer(text="Please reply with the corresponding guild number.")

        await ctx.send(embed=embed)

        try:
            reply = await self.bot.wait_for(
                "message",
                timeout=30,
                check=MessagePredicate.valid_int(ctx),
            )

            index = int(reply.content) - 1
            if 0 <= index < len(guilds):
                return guilds[index]
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond. Please try again.")

        return None

    @commands.Cog.listener()
    async def on_message_without_command(self, message: discord.Message):
        """Detect venting messages and process them."""
        if not isinstance(message.channel, discord.DMChannel):
            return

        author = message.author
        guilds = await self.discover_guild(author)
        if not guilds:
            return

        if author.id in self.user_cache:
            return

        vent = await self.config.custom("VENT").get_raw(message.guild.id, default=None)
        if vent is not None:
            return

        guild = None
        if len(guilds) > 1:
            guild = await self.send_discoverable_guilds(message, guilds)
            if guild is None:
                return
        else:
            guild = guilds[0]

        self.user_cache.append(author.id)

        if guild is not None:
            await self.process_venting(author, guild, message)

    async def process_venting(self, author: discord.User, guild: discord.Guild, message: discord.Message):
        """Process the venting message."""
        output_channel = await self.config.guild(guild).output_channel()
        if output_channel is None:
            return

        self.antispam.setdefault(author.id, AntiSpam(self.intervals))
        if not self.antispam[author.id].is_spamming():
            embed = discord.Embed(
                title=_("Anonymous Vent"),
                description=message.content,
                color=discord.Color.blurple(),
            )
            embed.set_footer(text=_("User ID: {}").format(author.id))

            with contextlib.suppress(discord.NotFound, discord.Forbidden):
                channel = guild.get_channel(output_channel)
                if channel is not None:
                    await channel.send(embed=embed)

            await self.antispam[author.id].stamp()
            await self.update_user_cache()

    async def update_user_cache(self):
        """Update the user cache after a cooldown."""
        await asyncio.sleep(300)
        self.user_cache = [user for user in self.user_cache if self.antispam.get(user, None) is not None]

    @commands.guild_only()
    @commands.group(name="vent", invoke_without_command=True)
    async def vent(self, ctx: commands.Context):
        """Vent anonymously."""
        active = await self.config.guild(ctx.guild).active()
        if active:
            output_channel = await self.config.guild(ctx.guild).output_channel()
            await ctx.send(
                _("Venting is currently active in this server. Messages will be sent to <#{channel}>.").format(
                    channel=output_channel
                )
            )
        else:
            await ctx.send(_("Venting is not currently active in this server."))

    @vent.command(name="toggle")
    @commands.has_permissions(manage_channels=True)
    async def vent_toggle(self, ctx: commands.Context):
        """Toggle venting in this server."""
        active = await self.config.guild(ctx.guild).active()
        active = not active
        await self.config.guild(ctx.guild).active.set(active)
        if active:
            await ctx.send(_("Venting is now active in this server."))
        else:
            await ctx.send(_("Venting is no longer active in this server."))

    @vent.command(name="setchannel")
    @commands.has_permissions(manage_channels=True)
    async def vent_set_channel(self, ctx: commands.Context, channel: discord.TextChannel):
        """Set the channel where venting messages will be sent."""
        await self.config.guild(ctx.guild).output_channel.set(channel.id)
        await ctx.send(_("Venting output channel set to {channel}.").format(channel=channel.mention))

    @vent.command(name="show")
    async def vent_show(self, ctx: commands.Context):
        """Show the current venting configuration."""
        active = await self.config.guild(ctx.guild).active()
        output_channel_id = await self.config.guild(ctx.guild).output_channel()
        output_channel = ctx.guild.get_channel(output_channel_id) if output_channel_id else None

        if active:
            if output_channel:
                output_channel_text = output_channel.mention
            else:
                output_channel_text = _("Not set")
        else:
            output_channel_text = _("Not active")

        msg = _(
            "Venting is {active}\n"
            "Output channel: {output_channel}"
        ).format(
            active=active,
            output_channel=output_channel_text,
        )

        await ctx.send(msg)

    @vent.command(name="setmessage")
    @commands.has_permissions(manage_channels=True)
    async def vent_set_message(self, ctx: commands.Context, *, message: str):
        """Set a default vent message."""
        vent = await self.config.custom("VENT").get_raw(ctx.guild.id, default=None)
        if vent is not None:
            await ctx.send(_("The default vent message is already set."))
        else:
            await self.config.custom("VENT").set_raw(ctx.guild.id, value={"message": message})
            await ctx.send(_("Default vent message set."))

    @vent.command(name="unsetmessage")
    @commands.has_permissions(manage_channels=True)
    async def vent_unset_message(self, ctx: commands.Context):
        """Unset the default vent message."""
        vent = await self.config.custom("VENT").get_raw(ctx.guild.id, default=None)
        if vent is None:
            await ctx.send(_("The default vent message is already unset."))
        else:
            await self.config.custom("VENT").clear_raw(ctx.guild.id)
            await ctx.send(_("Default vent message unset."))

    @vent.command(name="setticket")
    @commands.has_permissions(manage_channels=True)
    async def vent_set_ticket(self, ctx: commands.Context, ticket: int):
        """Set the next vent ticket number."""
        if ticket < 1:
            await ctx.send(_("The ticket number must be greater than 0."))
        else:
            await self.config.guild(ctx.guild).next_ticket.set(ticket)
            await ctx.send(_("The next vent ticket number has been set to {}.").format(ticket))

    @vent.command(name="ticket")
    @commands.has_permissions(manage_channels=True)
    async def vent_ticket(self, ctx: commands.Context):
        """Get the next vent ticket number."""
        next_ticket = await self.config.guild(ctx.guild).next_ticket()
        await ctx.send(_("The next vent ticket number is {}.").format(next_ticket))

    @vent.command(name="list")
    @commands.has_permissions(manage_channels=True)
    async def vent_list(self, ctx: commands.Context):
        """List all active vent channels and their respective ticket numbers."""
        guild_settings = await self.config.all_guilds()
        vent_channels = {
            guild_id: settings["output_channel"]
            for guild_id, settings in guild_settings.items()
            if settings["active"]
        }
        if not vent_channels:
            await ctx.send(_("There are no active vent channels."))
            return

        guilds = self.bot.get_guilds()
        vent_channels_list = [
            (guilds[int(guild_id)].name, channel_id)
            for guild_id, channel_id in vent_channels.items()
        ]
        vent_channels_list.sort()

        embed = discord.Embed(title=_("Active Vent Channels"), colour=await ctx.embed_colour())
        for guild_name, channel_id in vent_channels_list:
            channel = ctx.guild.get_channel(channel_id)
            if channel:
                embed.add_field(
                    name=guild_name,
                    value=channel.mention,
                    inline=False,
                )
            else:
                embed.add_field(
                    name=guild_name,
                    value=_("Channel ID: {}").format(channel_id),
                    inline=False,
                )

        await ctx.send(embed=embed)

    @vent.command(name="tunnel")
    @commands.has_permissions(manage_channels=True)
    async def vent_tunnel(self, ctx: commands.Context, guild_id: int, channel_id: int):
        """Tunnel a vent message to a specific guild and channel."""
        try:
            guild = self.bot.get_guild(guild_id)
            channel = guild.get_channel(channel_id)
        except (AttributeError, TypeError):
            await ctx.send(_("Invalid guild or channel ID."))
            return

        if guild is None or channel is None:
            await ctx.send(_("Invalid guild or channel ID."))
            return

        with Tunnel(self.bot):
            await self.process_venting(ctx.author, guild, copy(ctx.message))

    @vent.command(name="help")
    async def vent_help(self, ctx: commands.Context):
        """Display venting help message."""
        prefix = ctx.clean_prefix
        help_msg = _(
            "To vent anonymously, simply send a direct message to me (the bot).\n\n"
            "You can also use the following commands:\n\n"
            "{prefix}vent toggle: Toggle venting in this server.\n"
            "{prefix}vent setchannel <channel>: Set the channel where venting messages will be sent.\n"
            "{prefix}vent show: Show the current venting configuration.\n"
            "{prefix}vent setmessage <message>: Set a default vent message.\n"
            "{prefix}vent unsetmessage: Unset the default vent message.\n"
            "{prefix}vent setticket <ticket>: Set the next vent ticket number.\n"
            "{prefix}vent ticket: Get the next vent ticket number.\n"
            "{prefix}vent list: List all active vent channels and their respective ticket numbers.\n"
            "{prefix}vent tunnel <guild_id> <channel_id>: Tunnel a vent message to a specific guild and channel.\n"
            "{prefix}vent help: Display this help message."
        ).format(prefix=prefix)

        await ctx.send(box(help_msg))

    async def _cleanup(self):
        await super().cog_unload()
        for spam in self.antispam.values():
            if hasattr(spam, "_task"):
                spam._task.cancel()
        self.antispam.clear()

    def cog_unload(self):
        asyncio.create_task(self._cleanup())
        return super().cog_unload()
