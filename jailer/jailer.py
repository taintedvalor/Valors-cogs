import discord
from redbot.core import commands, Config
from discord.ext import tasks
from io import BytesIO

class MMedia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=959327177)
        default_guild_settings = {
            "designated_channel": None,
            "ignored_entities": []  # A list to store both users and roles to be ignored
        }
        self.config.register_guild(**default_guild_settings)
        self.image_check.start()

    def cog_unload(self):
        self.image_check.cancel()

    def has_higher_permission():
        async def predicate(ctx):
            if ctx.guild is None:
                return False
            return ctx.author.guild_permissions.manage_guild

        return commands.check(predicate)

    @commands.group()
    async def MMedia(self, ctx):
        """Manage MMedia cog settings."""
        pass

    @MMedia.command()
    @has_higher_permission()
    async def set_channel(self, ctx, channel: discord.TextChannel):
        """Set the designated channel for moving media."""
        await self.config.guild(ctx.guild).designated_channel.set(channel.id)
        await ctx.send(f"Designated channel set to {channel.mention}.")

    @MMedia.command()
    @has_higher_permission()
    async def ignore(self, ctx, entity: discord.User or discord.Role):
        """Add a user or role to the ignore list."""
        async with self.config.guild(ctx.guild).ignored_entities() as ignored_entities:
            ignored_entities.append(entity.id)
        await ctx.send(f"{entity.mention} added to the ignore list.")

    @MMedia.command()
    @has_higher_permission()
    async def unignore(self, ctx, entity: discord.User or discord.Role):
        """Remove a user or role from the ignore list."""
        async with self.config.guild(ctx.guild).ignored_entities() as ignored_entities:
            ignored_entities.remove(entity.id)
        await ctx.send(f"{entity.mention} removed from the ignore list.")

    @tasks.loop(seconds=10)
    async def image_check(self):
        for guild in self.bot.guilds:
            designated_channel = await self.config.guild(guild).designated_channel()
            if not designated_channel:
                continue

            ignored_entities = await self.config.guild(guild).ignored_entities()
            destination_channel = guild.get_channel(designated_channel)

            for channel in guild.text_channels:
                if channel.id == designated_channel:
                    continue

                async for message in channel.history(limit=1):
                    if (
                        message.attachments
                        and message.author.id not in ignored_entities
                        and not any(role.id in ignored_entities for role in message.author.roles)
                    ):
                        original_poster = message.author.mention
                        text_content = message.content
                        image_url = message.attachments[0].url
                        await message.delete()
                        await self.move_media_with_text(destination_channel, original_poster, text_content, image_url)
                        break

    async def move_media_with_text(self, destination_channel, original_poster, text_content, image_url):
        async with self.bot.session.get(image_url) as response:
            if response.status != 200:
                return

            image_bytes = await response.read()

        img = BytesIO(image_bytes)
        filename = image_url.split("/")[-1]
        media_with_text = f"{original_poster}\n{text_content}" if text_content else original_poster

        await destination_channel.send(content=media_with_text, file=discord.File(img, filename=filename))

def setup(bot):
    bot.add_cog(MMedia(bot))
