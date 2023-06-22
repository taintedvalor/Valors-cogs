from redbot.core import commands, checks, Config
from redbot.core.i18n import cog_i18n, Translator

import discord
import asyncio
from typing import Optional

_ = Translator("AnonReporter", __file__)


@cog_i18n(_)
class AnonReporter(commands.Cog):
    __version__ = "2.0.0"

    def format_help_for_context(self, ctx: commands.Context) -> str:
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, *, user_id, requester):
        return  # This cog stores no EUD

    def __init__(self, bot):
        self.config = Config.get_conf(self, identifier=171814082020, force_registration=True)
        default_guild = {"channel": None}
        default_global = {"rep_guild": None, "rep_channel": None}
        self.bot = bot
        self.config.register_guild(**default_guild)
        self.config.register_global(**default_global)

    @commands.group()
    async def anonreporter(self, ctx):
        """Anonreporter settings"""
        pass

    @anonreporter.command()
    async def channel(self, ctx, channel: discord.TextChannel):
        """Set the channel used for guild reports."""
        await self.config.guild(ctx.guild).channel.set(channel.id)
        await ctx.send(_("Report channel set to {channel}").format(channel=channel.mention))

    @checks.is_owner()
    @anonreporter.command(name="global")
    async def global_channel(self, ctx, channel: discord.TextChannel):
        """Set the channel for global reports."""
        await self.config.rep_guild.set(ctx.guild.id)
        await self.config.rep_channel.set(channel.id)
        await ctx.send(
            _("Global reports channel set to {channel} in {guild}").format(
                channel=channel.mention, guild=ctx.guild.name
            )
        )

    @commands.command()
    async def anonvent(self, ctx, *, text: Optional[str]):
        """Vent something anonymously (don't include text to vent via DM)"""

        def msgcheck(m):
            return m.guild is None and m.author.id == ctx.author.id

        if not text:
            try:
                await ctx.author.send(_("Send your vent here. You have 120s."))
                text = (
                    await self.bot.wait_for("message", check=msgcheck, timeout=120)
                ).content
            except discord.HTTPException:
                await ctx.send(
                    _("Sending a DM failed. Make sure you allow DMs from the bot."),
                    delete_after=15,
                )
            except asyncio.TimeoutError:
                await ctx.author.send(_("Action timed out."))
        else:
            if channel := await self.config.guild(ctx.guild).channel():
                await ctx.message.delete(delay=15)
            else:
                await self._send_not_configured_correctly_message(ctx.channel)
                return

        if 0 < len(text) < 1000:
            report_channel = ctx.guild.get_channel(channel)
            if report_channel:
                await report_channel.send(
                    _("**New anonymous vent:**\n{vent}").format(vent=text)
                )
                await ctx.tick()
            else:
                await self._send_not_configured_correctly_message(ctx.channel)
        else:
            await ctx.send(_("Text too short or too long."), delete_after=15)

    async def _send_not_configured_correctly_message(self, messageable):
        await messageable
