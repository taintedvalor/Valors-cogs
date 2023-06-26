import asyncio
import io
import datetime

import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import box

from utilities.ai_utils import generate_response, search, get_yt_transcript
from utilities.response_util import split_response, translate_to_en, get_random_prompt
from utilities.config_loader import config, load_current_language, load_instructions
from utilities.sanitization_utils import sanitize_prompt

class ChatBotCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.allow_dm = config['ALLOW_DM']
        self.active_channels = set()
        self.trigger_words = config['TRIGGER']
        self.smart_mention = config['SMART_MENTION']
        self.presences = config["PRESENCES"]
        self.message_history = {}
        self.MAX_HISTORY = config['MAX_HISTORY']
        self.personaname = config['INSTRUCTIONS'].title()
        self.replied_messages = {}
        self.current_language = load_current_language()
        self.instruction = {}
        load_instructions(self.instruction)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()
        self.presences_cycle = cycle(self.presences)
        print(f"{self.bot.user} aka {self.bot.user.name} has connected to Discord!")
        invite_link = discord.utils.oauth_url(
            self.bot.user.id,
            permissions=discord.Permissions(),
            scopes=("bot", "applications.commands")
        )
        print(f"Invite link: {invite_link}")
        while True:
            presence = next(self.presences_cycle)
            presence_with_count = presence.replace("{guild_count}", str(len(self.bot.guilds)))
            delay = config['PRESENCES_CHANGE_DELAY']
            await self.bot.change_presence(activity=discord.Game(name=presence_with_count))
            await asyncio.sleep(delay)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user and message.reference:
            self.replied_messages[message.reference.message_id] = message
            if len(self.replied_messages) > 5:
                oldest_message_id = min(self.replied_messages.keys())
                del self.replied_messages[oldest_message_id]

        if message.stickers or message.author.bot or (message.reference and (message.reference.resolved.author != self.bot.user or message.reference.resolved.embeds)):
            return

        is_replied = (message.reference and message.reference.resolved.author == self.bot.user) and self.smart_mention
        is_dm_channel = isinstance(message.channel, discord.DMChannel)
        is_active_channel = message.channel.id in self.active_channels
        is_allowed_dm = self.allow_dm and is_dm_channel
        contains_trigger_word = any(word in message.content for word in self.trigger_words)
        is_bot_mentioned = self.bot.user.mentioned_in(message) and self.smart_mention and not message.mention_everyone
        bot_name_in_message = self.bot.user.name.lower() in message.content.lower() and self.smart_mention

        if is_active_channel or is_allowed_dm or contains_trigger_word or is_bot_mentioned or is_replied or bot_name_in_message:
            channel_id = message.channel.id
            key = f"{message.author.id}-{channel_id}"

            if key not in self.message_history:
                self.message_history[key] = []

            self.message_history[key] = self.message_history[key][-self.MAX_HISTORY:]

            has_file = False
            file_content = None

            for attachment in message.attachments:
                file_content = f"The user has sent a file"
                has_file = True
                break

            message_content = message.content if not has_file else file_content
            message_content = message_content.strip()

            if not message_content:
                return

            self.message_history[key].append(message_content)
            user_message = message_content.lower()
            sanitized_prompt = sanitize_prompt(user_message)

            async with message.channel.typing():
                response = await generate_response(sanitized_prompt, self.current_language)

            if not response:
                response = await search(sanitized_prompt, self.current_language)

            if not response:
                response = await get_yt_transcript(sanitized_prompt, self.current_language)

            if not response:
                response = await generate_response(get_random_prompt(), self.current_language)

            response = sanitize_prompt(response)

            if self.current_language != "en":
                response = await translate_to_en(response)

            response_parts = split_response(response)
            for response_part in response_parts:
                response_message = await message.channel.send(response_part)

                if message.reference:
                    replied_message = self.replied_messages.get(message.reference.message_id)
                    if replied_message:
                        await response_message.reply(f"In response to {replied_message.author.mention}:")
                        self.replied_messages.pop(message.reference.message_id)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandNotFound):
            return

        raise error

    @commands.command()
    async def ping(self, ctx):
        """Check the bot's response time."""
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

def setup(bot):
    bot.add_cog(ChatBotCog(bot))
