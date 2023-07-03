import discord
from redbot.core import commands, Config, checks

class VoiceActivity(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)  # Use a unique identifier
        default_guild_settings = {
            "voice_channel_id": None,
            "activity_mapping": {
                "playing": "Playing",
                "streaming": "Streaming",
                "listening": "Listening",
                "watching": "Watching"
            }
        }
        self.config.register_guild(**default_guild_settings)
        self.update_activity.start()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        voice_channel_id = await self.config.guild(member.guild).voice_channel_id()
        if voice_channel_id is not None and voice_channel_id == after.channel.id:
            await self.update_voice_channel_name(member.guild)

    async def update_voice_channel_name(self, guild):
        voice_channel_id = await self.config.guild(guild).voice_channel_id()
        voice_channel = guild.get_channel(voice_channel_id)
        if voice_channel is None or not isinstance(voice_channel, discord.VoiceChannel):
            return

        members = voice_channel.members
        if members:
            activity = members[0].activity
            if activity is not None and isinstance(activity, discord.Activity):
                activity_type = str(activity.type)
                activity_name = activity.name
                activity_mapping = await self.config.guild(guild).activity_mapping()
                new_channel_name = f"{activity_mapping.get(activity_type, 'Unknown')}: {activity_name}"
                if new_channel_name != voice_channel.name:
                    await voice_channel.edit(name=new_channel_name)

    @commands.group()
    @commands.guild_only()
    @checks.admin()
    async def voiceactivity(self, ctx):
        """Manage voice activity settings."""
        pass

    @voiceactivity.command(name="setchannel")
    async def set_voice_channel(self, ctx, channel: discord.VoiceChannel):
        """Sets the voice channel for activity updates."""
        await self.config.guild(ctx.guild).voice_channel_id.set(channel.id)
        await ctx.send(f"The voice channel for activity updates has been set to {channel.mention}.")

    @voiceactivity.command(name="activitymapping")
    async def set_activity_mapping(self, ctx, activity_type: str, display_name: str):
        """Sets the mapping for activity types."""
        activity_mapping = await self.config.guild(ctx.guild).activity_mapping()
        activity_mapping[activity_type] = display_name
        await self.config.guild(ctx.guild).activity_mapping.set(activity_mapping)
        await ctx.send("Activity mapping updated.")

    @voiceactivity.command(name="resetmapping")
    async def reset_activity_mapping(self, ctx):
        """Resets the activity mapping to default."""
        default_activity_mapping = {
            "playing": "Playing",
            "streaming": "Streaming",
            "listening": "Listening",
            "watching": "Watching"
        }
        await self.config.guild(ctx.guild).activity_mapping.set(default_activity_mapping)
        await ctx.send("Activity mapping reset to default.")

    @voiceactivity.command(name="removechannel")
    async def remove_voice_channel(self, ctx):
        """Removes the voice channel for activity updates."""
        await self.config.guild(ctx.guild).voice_channel_id.set(None)
        await ctx.send("The voice channel for activity updates has been removed.")

    @voiceactivity.command(name="showconfig")
    async def show_config(self, ctx):
        """Shows the current voice activity configuration."""
        voice_channel_id = await self.config.guild(ctx.guild).voice_channel_id()
        channel_mention = ctx.guild.get_channel(voice_channel_id).mention if voice_channel_id else "Not set"
        activity_mapping = await self.config.guild(ctx.guild).activity_mapping()
        config_message = f"Voice Channel: {channel_mention}\n\nActivity Mapping:\n"
        for activity_type, display_name in activity_mapping.items():
            config_message += f"{activity_type}: {display_name}\n"
        await ctx.send(config_message)

    @tasks.loop(seconds=60)
    async def update_activity(self):
        guilds = self.bot.guilds
        for guild in guilds:
            voice_channel_id = await self.config.guild(guild).voice_channel_id()
            if voice_channel_id is not None:
                await self.update_voice_channel_name(guild)

    def cog_unload(self):
        self.update_activity.cancel()

def setup(bot):
    bot.add_cog(VoiceActivity(bot))
