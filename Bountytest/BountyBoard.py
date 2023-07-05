import asyncio
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

# Example StarBoard class
class StarBoard:
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)
        default_guild_config = {
            "stars": {}  # {user_id: star_count}
        }
        self.config.register_guild(**default_guild_config)

    async def add_star(self, user):
        star_count = await self.get_star_count(user)
        star_count += 1
        await self.config.stars.set_raw(user.id, value=star_count)

    async def get_star_count(self, user):
        star_count = await self.config.stars.get_raw(user.id, default=0)
        return star_count

    @commands.command(name="stars")
    async def show_stars(self, ctx, user=None):
        if user is None:
            user = ctx.author
        else:
            try:
                user = await commands.UserConverter().convert(ctx, user)
            except commands.errors.BadArgument:
                await ctx.send("User not found.")
                return

        star_count = await self.get_star_count(user)
        await ctx.send(f"{user.mention} has {star_count} stars.")

# Example BountyBoard cog
class BountyBoard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)
        default_guild_config = {
            "supervisor_role": None,
            "bounty_channel": None,
            "ask_reward": True,
            "ask_supervisor": True
        }
        self.config.register_guild(**default_guild_config)
        self.bounties = []
        self.starboard = StarBoard(bot)

    async def update_bounty_board(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            await self.update_board_messages()
            await asyncio.sleep(5)  # Update every 5 seconds

    async def update_board_messages(self):
        for guild in self.bot.guilds:
            bounty_channel_id = await self.config.guild(guild).bounty_channel()
            if bounty_channel_id:
                bounty_channel = guild.get_channel(bounty_channel_id)
                if bounty_channel:
                    await self.send_bounty_board(guild, bounty_channel)

    async def send_bounty_board(self, guild, channel):
        if not self.bounties:
            await channel.send("There are no active bounties.")
            return

        embed = Embed(title="Bounty Board", description="Current Bounties")

        for idx, bounty in enumerate(self.bounties):
            status_emoji = "✅" if not bounty.taken else "⌛"
            embed.add_field(
                name=f"**{idx + 1}. {bounty.name}**",
                value=f"Description: {bounty.description}\nReward: {bounty.reward}\nStatus: {status_emoji}",
                inline=False,
            )

        await channel.send(embed=embed)

    @commands.group(name="bounty", aliases=["bounties"], invoke_without_command=True)
    async def bounty_group(self, ctx):
        """Manage bounties"""
        await ctx.send_help()

    @bounty_group.command(name="create")
    async def create_bounty(self, ctx, name, *, description):
        # Request reward from user
        ask_reward = await self.config.guild(ctx.guild).ask_reward()
        if ask_reward:
            reward_msg: Message = await ctx.send("Would you like to set a reward for this bounty? (Type 'no' to skip)")
            reward_response = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)

            if reward_response.content.lower() == "no":
                reward = None
                await reward_msg.delete()
            else:
                reward = reward_response.content

                await reward_msg.delete()
                await reward_response.delete()
        else:
            reward = None

        # Request supervisor from user
        ask_supervisor = await self.config.guild(ctx.guild).ask_supervisor()
        if ask_supervisor:
            supervisor = None  # Assign None as the default value
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
        else:
            supervisor = None

        bounty = Bounty(name, description, ctx.author)
        bounty.reward = reward
        bounty.supervisor = supervisor

        self.bounties.append(bounty)

        await ctx.send(f"**Bounty created!**\nName: {name}\nDescription: {description}\nReward: {reward}")

    @bounty_group.command(name="complete")
    async def complete_bounty(self, ctx, bounty_name):
        for bounty in self.bounties:
            if bounty.name.lower() == bounty_name.lower():
                if not bounty.completed:
                    if ctx.author == bounty.poster or ctx.author == bounty.supervisor:
                        bounty.completed = True
                        self.bounties.remove(bounty)
                        await ctx.send(f"Bounty '{bounty.name}' has been marked as completed by {ctx.author.mention}.")
                        await self.starboard.add_star(ctx.author)
                        await bounty.poster.send(f"Your bounty '{bounty.name}' has been completed by {ctx.author.mention}.")
                    else:
                        await ctx.send("Only the bounty poster or a supervisor can complete a bounty.")
                    return

        await ctx.send("Bounty not found!")

    @bounty_group.command(name="board")
    async def bounty_board(self, ctx):
        await self.send_bounty_board(ctx.guild, ctx.channel)

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
                    await ctx.send(f"{bounty.poster.mention} posted this bounty. Please contact them for further details.")
                    await bounty.poster.send(f"Your bounty '{bounty.name}' has been taken up by {ctx.author.mention} and is now pending.")
                    return
                else:
                    await ctx.send("This bounty has already been taken.")
                    return

        await ctx.send("Bounty not found!")

    @bounty_group.command(name="set_channel")
    @checks.admin_or_permissions(manage_channels=True)
    async def set_bounty_channel(self, ctx, channel: commands.TextChannelConverter):
        await self.config.guild(ctx.guild).bounty_channel.set(channel.id)
        await ctx.send(f"The bounty channel has been set as {channel.mention}.")
        await self.send_bounty_board(ctx.guild, channel)

    @commands.Cog.listener()
    async def on_ready(self):
        print("BountyBoard cog loaded.")
        self.bot.loop.create_task(self.update_bounty_board())

# Bot setup
def setup(bot):
    bot.add_cog(BountyBoard(bot))
    bot.add_cog(StarBoard(bot))
