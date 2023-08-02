import discord
from redbot.core import commands, Config
from discord.ext import tasks

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

    @commands.group()
    async def MMedia(self, ctx):
        """Manage MMedia cog settings."""
        pass

    @MMedia.command()
    async def set_channel(self, ctx, channel: discord.TextChannel):
        """Set the designated channel for moving media."""
        await self.config.guild(ctx.guild).designated_channel.set(channel.id)
        await ctx.send(f"Designated channel set to {channel.mention}.")

    @MMedia.command()
    async def ignore(self, ctx, entity: discord.User or discord.Role):
        """Add a user or role to the ignore list."""
        async with self.config.guild(ctx.guild).ignored_entities() as ignored_entities:
            ignored_entities.append(entity.id)
        await ctx.send(f"{entity.mention} added to the ignore list.")

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

                async for message in channel.history(limit=50):
                    if (
                        message.attachments
                        and not message.content
                        and message.author.id not in ignored_entities
                        and not any(role.id in ignored_entities for role in message.author.roles)
                    ):
                        original_poster = message.author.mention
                        media_url = message.attachments[0].url

                        await message.delete()

                        # Remove the original image and post a message in the offending channel
                        await channel.send(f"{original_poster}, your media has been moved to {destination_channel.mention}:\n{media_url}")
                        break

def setup(bot):
    bot.add_cog(MMedia(bot))
