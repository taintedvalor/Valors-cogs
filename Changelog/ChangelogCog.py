import discord
from redbot.core import commands
from redbot.core import Config

class ChangelogCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890, force_registration=True)
        self.config.register_guild(channels={})

    @commands.group(name="changelog", invoke_without_command=True)
    async def changelog(self, ctx):
        await ctx.send("Use subcommands: note, review, delete, setchannel, list, view")

    @changelog.command()
    async def note(self, ctx, modpack, version, *, note):
        changelogs = await self.config.guild(ctx.guild).channels()
        if ctx.channel.id in changelogs:
            channel_id = changelogs[ctx.channel.id]
            channel = self.bot.get_channel(channel_id)
            if modpack not in channel.name:
                await ctx.send("The modpack name must be part of the channel's name.")
                return
            version_notes = await self.config.guild(ctx.guild).version_notes()
            if modpack not in version_notes:
                version_notes[modpack] = {}
            if version not in version_notes[modpack]:
                version_notes[modpack][version] = []
            version_notes[modpack][version].append(note)
            await self.config.guild(ctx.guild).version_notes.set(version_notes)
            await ctx.send(f"Added note to {modpack} version {version} in {channel.mention}.")
        else:
            await ctx.send("This channel is not associated with a changelog category. Use the setchannel command to associate it.")

    @changelog.command()
    async def review(self, ctx, modpack):
        changelogs = await self.config.guild(ctx.guild).channels()
        if ctx.channel.id in changelogs:
            channel_id = changelogs[ctx.channel.id]
            channel = self.bot.get_channel(channel_id)
            version_notes = await self.config.guild(ctx.guild).version_notes()
            if modpack in version_notes:
                notes = version_notes[modpack]
                if notes:
                    response = f"**{channel.name} Changelog for {modpack}**:\n"
                    for version, note_list in notes.items():
                        response += f"**Version {version}**:\n"
                        for note in note_list:
                            response += f"{note}\n"
                    await ctx.send(response)
                else:
                    await ctx.send(f"No notes found for {modpack} in {channel.mention}.")
            else:
                await ctx.send(f"No changelog found for {modpack} in {channel.mention}.")
        else:
            await ctx.send("This channel is not associated with a changelog category. Use the setchannel command to associate it.")

    @changelog.command()
    async def delete(self, ctx, modpack, version):
        changelogs = await self.config.guild(ctx.guild).channels()
        if ctx.channel.id in changelogs:
            channel_id = changelogs[ctx.channel.id]
            channel = self.bot.get_channel(channel_id)
            version_notes = await self.config.guild(ctx.guild).version_notes()
            if modpack in version_notes and version in version_notes[modpack]:
                del version_notes[modpack][version]
                await self.config.guild(ctx.guild).version_notes.set(version_notes)
                await ctx.send(f"Deleted version {version} from {modpack} changelog in {channel.mention}.")
            else:
                await ctx.send(f"No such changelog version found in {channel.mention}.")
        else:
            await ctx.send("This channel is not associated with a changelog category. Use the setchannel command to associate it.")

    @changelog.command()
    async def setchannel(self, ctx):
        changelogs = await self.config.guild(ctx.guild).channels()
        changelogs[ctx.channel.id] = ctx.channel.category.id
        await self.config.guild(ctx.guild).channels.set(changelogs)
        await ctx.send(f"Channel {ctx.channel.mention} is now associated with a changelog category.")

    @changelog.command()
    async def list(self, ctx):
        changelogs = await self.config.guild(ctx.guild).channels()
        categories = set(changelogs.values())
        if categories:
            response = "Changelog categories:\n"
            for category_id in categories:
                category = self.bot.get_channel(category_id)
                response += f"{category.name}\n"
            await ctx.send(response)
        else:
            await ctx.send("No changelog categories found.")

    @changelog.command()
    async def view(self, ctx, channel_id_or_name):
        changelogs = await self.config.guild(ctx.guild).channels()
        if ctx.channel.id in changelogs:
            if channel_id_or_name in changelogs:
                channel_id = changelogs[channel_id_or_name]
            else:
                channel = discord.utils.get(ctx.guild.text_channels, name=channel_id_or_name)
                if channel:
                    channel_id = changelogs[channel.name]
                else:
                    await ctx.send("Channel not found.")
                    return
            version_notes = await self.config.guild(ctx.guild).version_notes()
            if channel.name in version_notes:
                notes = version_notes[channel.name]
                if notes:
                    response = f"**{channel.name} Changelog**:\n"
                    for modpack, versions in notes.items():
                        response += f"**Modpack: {modpack}**\n"
                        for version, note_list in versions.items():
                            response += f"**Version {version}**:\n"
                            for note in note_list:
                                response += f"{note}\n"
                    await ctx.send(response)
                else:
                    await ctx.send(f"No notes found in {channel.mention}.")
            else:
                await ctx.send(f"No changelogs found in {channel.mention}.")
        else:
            await ctx.send("This channel is not associated with a changelog category. Use the setchannel command to associate it.")

def setup(bot):
    bot.add_cog(ChangelogCog(bot))
