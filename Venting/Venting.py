import logging
import asyncio
from typing import List, Literal, Optional
from datetime import timedelta
from copy import copy
import contextlib
import discord

from redbot.core import Config, checks, commands
from redbot.core.utils import AsyncIter
from redbot.core.utils.chat_formatting import pagify, box
from redbot.core.utils.antispam import AntiSpam
from redbot.core.bot import Red
from redbot.core.i18n import Translator, cog_i18n, set_contextual_locales_from_guild
from redbot.core.utils.predicates import MessagePredicate

_ = Translator("Venting", __file__)

log = logging.getLogger("red.goon.Venting")


@cog_i18n(_)
class Venting(commands.Cog):
    """An anonymous Venting cog for users to express their feelings anonymously."""

    def __init__(self, bot: Red):
        super().__init__()
        self.bot = bot
        self.config = Config.get_conf(self, 78631113035100160, force_registration=True)
        self.config.register_guild(
            output_channel=None,
            active=False,
            next_ticket=1
        )
        self.antispam = {}

    async def red_delete_data_for_user(
        self,
        *,
        requester: Literal["discord_deleted_user", "owner", "user", "user_strict"],
        user_id: int
    ):
        if requester != "discord_deleted_user":
            return

        all_reports = await self.config.all_guilds()

        for guild_id, guild_data in all_reports.items():
            for ticket_number, ticket in guild_data.items():
                if ticket.get("user_id", 0) == user_id:
                    ticket["user_id"] = 0xDE1
                    ticket["report"] = "[REPORT DELETED DUE TO DISCORD REQUEST]"

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if isinstance(message.channel, discord.DMChannel):
            guilds = [
                guild
                for guild in self.bot.guilds
                if guild.get_member(message.author.id) is not None
            ]
            if not guilds:
                return

            for guild in guilds:
                g_active = await self.config.guild(guild).active()
                if not g_active:
                    continue

                if guild.id not in self.antispam:
                    self.antispam[guild.id] = {}

                if message.author.id not in self.antispam[guild.id]:
                    self.antispam[guild.id][message.author.id] = AntiSpam()

                if self.antispam[guild.id][message.author.id].spammy:
                    continue

                channel_id = await self.config.guild(guild).output_channel()
                channel = guild.get_channel(channel_id)
                if channel is None:
                    continue

                ticket_number = await self.config.guild(guild).next_ticket()
                await self.config.guild(guild).next_ticket.set(ticket_number + 1)

                report = message.content

                title = _("Anonymous Vent")
                desc = report

                if await self.bot.embed_requested(channel, message.author):
                    embed_colour = await self.bot.get_embed_colour(channel)
                    em = discord.Embed(description=desc, colour=embed_colour)
                    em.set_author(
                        name=title,
                        icon_url="https://cdn.discordapp.com/attachments/826191787991367721/826203765467381780/unknown.png",
                    )
                    footer = _("Vent #{}").format(ticket_number)
                    em.set_footer(text=footer)
                    send_as = "embed"
                else:
                    send_as = "content"

                try:
                    async with channel.typing():
                        await channel.send(content=desc, embed=em if send_as == "embed" else None)
                    await self.bot.send_filtered(
                        channel,
                        "Vent #{}: ".format(ticket_number) + _("Your anonymous Vent has been submitted."),
                    )
                    self.antispam[guild.id][message.author.id].stamp()
                except discord.Forbidden:
                    await self.bot.send_filtered(
                        message.author,
                        _("I'm sorry, but I couldn't send your Vent. Please contact a server admin."),
                    )
