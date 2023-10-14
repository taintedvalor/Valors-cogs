from redbot.core import commands

class Army(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_admin():
        async def predicate(ctx):
            # Check if the author is the bot owner
            is_bot_owner = await self.bot.is_owner(ctx.author)
            if is_bot_owner:
                return True

            # Check if the author has the Administrator permission
            return ctx.author.guild_permissions.administrator

        return commands.check(predicate)

    @commands.group(name='army', aliases=['Army'])
    async def army_group(self, ctx):
        """Manage army-related commands."""
        if ctx.invoked_subcommand is None:
            await ctx.send(f'Invalid army command. Use `{ctx.prefix}help army` for more information.')

    @army_group.command(name='rename_all')
    @is_admin()
    async def rename_all_members(self, ctx, *, new_name):
        """Rename all members in the guild."""
        for member in ctx.guild.members:
            try:
                await member.edit(nick=new_name)
            except discord.Forbidden:
                print(f"Unable to rename {member.display_name}")

    @army_group.command(name='reset_names')
    @is_admin()
    async def reset_all_names(self, ctx):
        """Reset the nicknames of all members in the guild."""
        for member in ctx.guild.members:
            try:
                await member.edit(nick=None)
            except discord.Forbidden:
                print(f"Unable to reset nickname for {member.display_name}")

def setup(bot):
    bot.add_cog(Army(bot))
