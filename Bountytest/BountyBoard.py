from discord import Embed, Message
from redbot.core import commands, Config, checks

# Example Bounty class
class Bounty:
    def __init__(self, name, description, poster):
        self.name = name
        self.description = description
        self.reward = None
        self.supervisor = None
        self.completed = False
        self.taken = False
        self.poster = poster

# Example BountyBoard cog
class BountyBoard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)
        default_guild_config = {
            "supervisor_role": None,
            "staticboard_channel": None
        }
        self.config.register_guild(**default_guild_config)
        self.bounties = []
        self.update_staticboard.start()

    def cog_unload(self):
        self.update_staticboard.cancel()

    @tasks.loop(minutes=1.0)
    async def update_staticboard(self):
        staticboard_channel_id = await self.config.guild(self.bot.guild).staticboard_channel()
        if staticboard_channel_id:
            staticboard_channel = self.bot.get_channel(staticboard_channel_id)
            if staticboard_channel:
                await self.update_staticboard_message(staticboard_channel)

    async def update_staticboard_message(self, channel):
        message = await channel.history().find(lambda m: m.author == self.bot.user)
        if not message:
            message = await channel.send("Bounty Board")

        embed = Embed(title="Bounty Board", description="Current Bounties")

        for idx, bounty in enumerate(self.bounties):
            status_emoji = "✅" if not bounty.taken else "⌛"
            embed.add_field(
                name=f"**{idx + 1}. {bounty.name}**",
                value=f"Description: {bounty.description}\nReward: {bounty.reward}\nStatus: {status_emoji}",
                inline=False,
            )

        await message.edit(content="", embed=embed)

    @commands.group(name="bounty", aliases=["bounties"], invoke_without_command=True)
    async def bounty_group(self, ctx):
        """Manage bounties"""
        await ctx.send_help()

    @bounty_group.command(name="create")
    async def create_bounty(self, ctx, name, *, description):
        # Request reward from user
        reward_msg: Message = await ctx.send("Would you like to set a reward for this bounty? (Type 'no' to skip)")
        reward_response = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)

        if reward_response.content.lower() == "no":
            reward = None
            await reward_msg.delete()
        else:
            reward = reward_response.content

        # Request supervisor from user
        supervisor_msg: Message = await ctx.send("Would you like to assign a supervisor for this bounty? (Type 'yes' or 'no')")
        supervisor_response = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)

        if supervisor_response.content.lower() == "yes":
            supervisor_role_id = await self.config.guild(ctx.guild).supervisor_role()
            if supervisor_role_id:
                supervisor_role = ctx.guild.get_role(supervisor_role_id)
                if supervisor_role:
                    supervisor_mention = supervisor_role.mention
                    await ctx.send(f"A supervisor role has been requested for this bounty. {supervisor_mention}")
                    supervisor = supervisor_role

        await supervisor_msg.delete()
        await supervisor_response.delete()

        bounty = Bounty(name, description, ctx.author)
        bounty.reward = reward
        bounty.supervisor = supervisor

        self.bounties.append(bounty)

        await ctx.send(f"**Bounty created!**\nName: {name}\nDescription: {description}\nReward: {reward}")

        staticboard_channel_id = await self.config.guild(ctx.guild).staticboard_channel()
        if staticboard_channel_id:
            staticboard_channel = self.bot.get_channel(staticboard_channel_id)
            if staticboard_channel:
                await self.update_staticboard_message(staticboard_channel)

    @bounty_group.command(name="complete")
    async def complete_bounty(self, ctx, bounty_name):
        for bounty in self.bounties:
            if bounty.name.lower() == bounty_name.lower():
                if not bounty.completed:
                    if ctx.author == bounty.poster or ctx.author == bounty.supervisor:
                        bounty.completed = True
                        self.bounties.remove(bounty)
                        await ctx.send(f"Bounty '{bounty.name}' has been marked as completed by {ctx.author.mention}.")
                        await bounty.poster.send(f"Your bounty '{bounty.name}' has been completed by {ctx.author.mention}.")
                    else:
                        await ctx.send("Only the bounty poster or a supervisor can complete a bounty.")
                    return

        await ctx.send("Bounty not found!")

    @bounty_group.command(name="board")
    async def bounty_board(self, ctx):
        if not self.bounties:
            await ctx.send("There are no active bounties.")
            return

        embed = Embed(title="Bounty Board", description="Current Bounties")

        for idx, bounty in enumerate(self.bounties):
            status_emoji = "✅" if not bounty.taken else "⌛"
            embed.add_field(
                name=f"**{idx + 1}. {bounty.name}**",
                value=f"Description: {bounty.description}\nReward: {bounty.reward}\nStatus: {status_emoji}",
                inline=False,
            )

        await ctx.send(embed=embed)

    @bounty_group.command(name="assign_supervisor")
    @checks.admin_or_permissions(manage_roles=True)
    async def assign_supervisor(self, ctx, supervisor: commands.RoleConverter):
        await self.config.guild(ctx.guild).supervisor_role.set(supervisor.id)
        await ctx.send(f"The supervisor role has been set as {supervisor.name}.")

    @bounty_group.command(name="take")
    async def take_bounty(self, ctx, bounty_name):
        for bounty in self.bounties:
            if bounty.name.lower() == bounty_name.lower():
                if not bounty.taken:
                    bounty.taken = True
                    await ctx.send(f"You have taken up the bounty '{bounty.name}'.")
                    await bounty.poster.send(f"Your bounty '{bounty.name}' has been taken up by {ctx.author.mention} and is now pending.")
                    return
                else:
                    await ctx.send("This bounty has already been taken.")
                    return

        await ctx.send("Bounty not found!")

    @commands.group(name="staticboard", invoke_without_command=True)
    @checks.admin()
    async def staticboard_group(self, ctx):
        """Manage the static bounty board"""
        await ctx.send_help()

    @staticboard_group.command(name="set")
    async def set_staticboard(self, ctx, channel: commands.TextChannelConverter):
        await self.config.guild(ctx.guild).staticboard_channel.set(channel.id)
        await ctx.send(f"The static bounty board has been set to {channel.mention}.")

    @staticboard_group.command(name="refresh")
    async def refresh_staticboard(self, ctx):
        staticboard_channel_id = await self.config.guild(ctx.guild).staticboard_channel()
        if staticboard_channel_id:
            staticboard_channel = self.bot.get_channel(staticboard_channel_id)
            if staticboard_channel:
                await self.update_staticboard_message(staticboard_channel)
                await ctx.send("The static bounty board has been refreshed.")

    @commands.Cog.listener()
    async def on_ready(self):
        print("BountyBoard cog loaded.")

# Bot setup
def setup(bot):
    bot.add_cog(BountyBoard(bot))
