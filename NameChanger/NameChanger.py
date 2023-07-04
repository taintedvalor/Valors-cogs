import discord
from redbot.core import commands, Config, checks, tasks

class NameChanger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)  # Replace with a unique identifier
        self.config.register_guild(voice_channel_id=None, check_interval=3)

        self.name_changer_task.start()

    def cog_unload(self):
        self.name_changer_task.cancel()

    @tasks.loop(minutes=1.0)
    async def name_changer_task(self):
        for guild in self.bot.guilds:
            voice_channel_id = await self.config.guild(guild).voice_channel_id()
            check_interval = await self.config.guild(guild).check_interval()

            if voice_channel_id:
                voice_channel = guild.get_channel(voice_channel_id)

                if voice_channel and isinstance(voice_channel, discord.VoiceChannel):
                    for member in voice_channel.members:
                        activity = member.activity

                        if activity and activity.name:
                            new_name = activity.name
                            if not voice_channel.name.startswith("Activity:") or voice_channel.name != new_name:
                                await voice_channel.edit(name=new_name)
                        else:
                            default_name = "No Activity"
                            if not voice_channel.name.startswith("Activity:") or voice_channel.name != default_name:
                                await voice_channel.edit(name=default_name)

        self.name_changer_task.change_interval(minutes=check_interval)

    @checks.admin_or_permissions(manage_channels=True)
    @commands.group()
    async def namechanger(self, ctx):
        """Group command for managing the voice channel name changer."""
        pass

    @namechanger.command()
    async def set(self, ctx, channel: discord.VoiceChannel):
        """Set the designated voice channel for automatic name changes."""
        await self.config.guild(ctx.guild).voice_channel_id.set(channel.id)
        await ctx.send(f"Voice channel set to {channel.name}.")

    @namechanger.command()
    async def clear(self, ctx):
        """Clear the designated voice channel for automatic name changes."""
        await self.config.guild(ctx.guild).voice_channel_id.clear()
        await ctx.send("Voice channel cleared.")

    @namechanger.command()
    async def interval(self, ctx, minutes: int):
        """Set the time interval (in minutes) between name change checks."""
        await self.config.guild(ctx.guild).check_interval.set(minutes)
        await ctx.send(f"Name change check interval set to {minutes} minutes.")

def setup(bot):
    bot.add_cog(NameChanger(bot))
