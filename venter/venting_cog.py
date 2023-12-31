import discord
from redbot.core import commands, bot
from typing import List
from fuzzywuzzy import process

BaseCog = getattr(commands, "Cog", object)

class VentCog(commands.Cog):
    def __init__(self, bot_instance: bot):
        self.bot = bot_instance
        self.venting_channels = {}
        self.pending_messages = {}

    @commands.group(invoke_without_command=True)
    async def venter(self, ctx):
        """Commands for anonymous venting."""
        pass

    @venter.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def setchannel(self, ctx, channel: discord.TextChannel):
        """Set the venting channel for anonymous messages."""
        guild_id = ctx.guild.id
        self.venting_channels[guild_id] = channel.id
        await ctx.send(f"Venting channel set to {channel.mention}.")

    @venter.command(name="vent", rest_is_raw=True)
    async def venter_vent(self, ctx, *, message: str = None):
        """Vent Anonymously from Dms to the configured venting channel or a specified guild."""
        if ctx.guild:
            await self.send_to_venting_channel(ctx, message)
        else:
            await self.send_to_guild(ctx, message)

    async def send_to_venting_channel(self, ctx, message: str):
        guild_id = ctx.guild.id
        vent_channel_id = self.venting_channels.get(guild_id)
        if not vent_channel_id:
            return await ctx.send("Venting channel not set for this guild.")

        target_channel = ctx.guild.get_channel(vent_channel_id)
        if not target_channel:
            return await ctx.send("The configured venting channel was not found.")

        attachments = ctx.message.attachments
        if not message and not attachments:
            return await ctx.send("Please provide a message or an attachment.")

        vent_message = f"Anonymous Person:\n{message}" if message else "Anonymous Person"
        files = [await attachment.to_file(spoiler=self.is_image_spoiler(attachment.filename)) for attachment in attachments]
        await target_channel.send(content=vent_message, files=files)
        await ctx.send("Your message has been sent.")

    async def send_to_guild(self, ctx, message: str):
        def check(m):
            return m.author == ctx.author and isinstance(m.channel, discord.DMChannel)

        await ctx.send("Please provide the name or ID of the guild to send the anonymous message:")
        try:
            response = await self.bot.wait_for("message", check=check, timeout=60)
        except asyncio.TimeoutError:
            return await ctx.send("You took too long to respond. Message sending canceled.")

        guild_name_or_id = response.content.strip()
        guild = self.find_guild(ctx, guild_name_or_id)
        if guild:
            vent_channel_id = self.venting_channels.get(guild.id)
            if not vent_channel_id:
                return await ctx.send("Venting channel not set for the specified guild.")

            target_channel = guild.get_channel(vent_channel_id)
            if not target_channel:
                return await ctx.send("The configured venting channel was not found in the specified guild.")

            await ctx.send("You can now start sending your anonymous messages. Respond with ✓ when you are done.")
            self.pending_messages[ctx.author.id] = {
                "target_channel": target_channel,
                "messages": [],
                "attachments": []
            }
        else:
            await ctx.send("Guild not found.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if (
            not message.guild
            and message.author != self.bot.user
            and message.author.id in self.pending_messages
        ):
            pending = self.pending_messages[message.author.id]
            if "inquiry_message" not in pending:
                if message.content == "✓":
                    await self.send_pending_messages(message.author.id)
                else:
                    pending["messages"].append(message.content)
                    pending["attachments"].extend(message.attachments)

    async def send_pending_messages(self, user_id):
        pending = self.pending_messages.pop(user_id, None)
        if not pending:
            return

        target_channel = pending["target_channel"]
        messages = pending["messages"]
        attachments = pending["attachments"]

        if not messages and not attachments:
            return

        vent_message = "Anonymous Person:\n" + "\n".join(messages)
        files = [await attachment.to_file(spoiler=self.is_image_spoiler(attachment.filename)) for attachment in attachments]
        await target_channel.send(content=vent_message, files=files)

    def find_guild(self, ctx, name_or_id):
        guild = discord.utils.find(lambda g: g.name == name_or_id or str(g.id) == name_or_id, ctx.bot.guilds)
        return guild

    def is_image_spoiler(self, filename: str) -> bool:
        image_extensions = [".png", ".jpg", ".jpeg", ".gif"]
        return any(filename.lower().endswith(ext) for ext in image_extensions)

def setup(bot):
    bot.add_cog(VentCog(bot))
