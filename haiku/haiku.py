import sys
import re

import discord
from redbot.core import commands, bot, Config
from redbot.core.utils import embed
import nltk
from nltk.corpus import cmudict
import syllables

from typing import List, Optional

nltk.download("cmudict")

BaseCog = getattr(commands, "Cog", object)


class Haiku(BaseCog):
    def __init__(self, bot_instance: bot):
        super().__init__()
        self.bot = bot_instance

        self.syllable_dict = cmudict.dict()
        self.custom_syllables = {
            'youre': 1,
            'theyre': 1,
            'cant': 1,
            'havent': 2,
        }

        self.log = {}
        self.quote_re = re.compile(r'\|\|([^\|]*)\|\|', re.DOTALL)

        self.config = Config.get_conf(self, identifier=1234567890)  # Replace with a unique identifier
        default_guild_settings = {
            "haikuenabled": True  # Initial state: Enabled
        }
        self.config.register_guild(**default_guild_settings)

        self.bot.add_listener(self.check_haiku, "on_message")
        self.bot.add_command(self.haikuenable)
        self.bot.add_command(self.haiku_disable)

    def get_syllables(self, message: str) -> List:
        message_content, _ = re.subn(r"\s+", " ", message)
        message_content, _ = re.subn(
            r"[^a-z ]", "", message_content, flags=re.IGNORECASE
        )
        message_syllables = []
        split_message = [w for w in message_content.split(" ") if w]
        for word in split_message:
            custom = self.custom_syllables.get(word.lower())
            cmu = self.syllable_dict.get(word.lower())
            if custom is not None:
                syll_count = custom
            elif cmu is not None:
                if not isinstance(cmu[0], str):
                    cmu = cmu[0]
                syll_count = len([w for w in cmu if w[-1].isdigit()])
            else:
                syll_count = syllables.estimate(word)

            message_syllables.append((word, syll_count))

        return message_syllables

    async def check_haiku(self, message: discord.Message):
        guild = message.guild
        haikuenabled = await self.config.guild(guild).haikuenabled()

        if not haikuenabled:
            return

        if message.author.bot:
            return

        if 'http' in message.clean_content:
            return

        # Rest of the method code...

    @commands.command()
    async def syllables(self, ctx, *msg: str):
        msg = " ".join(msg)
        syllables = self.get_syllables(msg)

        msg = [f"{word} ({count})" for word, count in syllables]
        msg = " ".join(msg)

        await ctx.send(msg)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def haikuenable(self, ctx):
        """Enable the haiku cog for this guild."""
        await self.config.guild(ctx.guild).haikuenabled.set(True)
        await ctx.send("Haiku cog has been enabled.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def haiku_disable(self, ctx):
        """Disable the haiku cog for this guild."""
        await self.config.guild(ctx.guild).haikuenabled.set(False)
        await ctx.send("Haiku cog has been disabled.")

    @commands.command()
    async def haikulog(self, ctx, msg_id: Optional[int] = None):
        message: discord.Message = ctx.message
        if message.reference:
            msg_id = message.reference.message_id

        if msg_id is None:
            return

        if msg_id in self.log:
            await ctx.send('\n'.join(str(_) for _ in self.log[msg_id]))


if __name__ == "__main__":
    import nltk
