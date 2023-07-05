import discord
from discord.ext import commands
from redbot.core import Config, checks

# Example Bounty class
class Bounty:
    def __init__(self, name, description, poster):
        self.name = name
        self.description = description
        self.poster = poster
        self.reward = None
        self.supervisor = None
        self.completed = False
        self.taken = False
        self.taken_by = None

# Example BountyBoard cog
class BountyBoard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)
        default_guild_config = {
            "supervisor_role": None,
            "bounty_channel": None,
            "toggle_reward": True,
            "toggle_supervisor": True
        }
        self.config.register_guild(**default_guild_config)
        self.bounties = []
        self.stars = {}  # Dictionary to store star counts

    async def send_bounty_board(self, guild, channel):
        embed = discord.Embed(title="Bounty Board", description="Active bounties")

        for bounty in self.bounties:
            embed.add_field(
                name=bounty.name,
                value=f"Poster: {bounty.poster.mention}\nDescription: {bounty.description}\nReward: {bounty.reward}",
                inline=False
            )

        await channel.send(embed=embed)

    async def take_bounty(self, ctx, bounty):
        if bounty.taken:
            await ctx.send("This bounty has already been taken.")
            return

        bounty.taken = True
        bounty.taken_by = ctx.author

        await ctx.send(f"{ctx.author.mention} has taken the bounty '{bounty.name}'.")
        await bounty.poster.send(f"{ctx.author.mention} has taken your bounty '{bounty.name}'.")

    @commands.group(name="bounty", aliases=["bounties"], invoke_without_command=True)
    async def bounty_group(self, ctx):
        """Manage bounties"""
        await ctx.send_help()

    @bounty_group.group(name="toggle", invoke_without_command=True)
    @checks.admin_or_permissions(manage_guild=True)
    async def toggle_group(self, ctx):
        """Toggle bounty options"""
        await ctx.send_help()

    @toggle_group.command(name="reward")
    async def toggle_reward(self, ctx):
        """Toggle the reward option for bounties"""
        current_state = await self.config.guild(ctx.guild).toggle_reward()
        await self.config.guild(ctx.guild).toggle_reward.set(not current_state)
        state = "enabled" if not current_state else "disabled"
        await ctx.send(f"The reward option for bounties has been {state}.")

    @toggle_group.command(name="supervisor")
    async def toggle_supervisor(self, ctx):
        """Toggle the supervisor option for bounties"""
        current_state = await self.config.guild(ctx.guild).toggle_supervisor()
        await self.config.guild(ctx.guild).toggle_supervisor.set(not current_state)
        state = "enabled" if not current_state else "disabled"
        await ctx.send(f"The supervisor option for bounties has been {state}.")

    @bounty_group.command(name="create")
    async def create_bounty(self, ctx, name, *, description):
        # Request reward from user if toggled on
        toggle_reward = await self.config.guild(ctx.guild).toggle_reward()
        if toggle_reward:
            reward_msg = await ctx.send("Would you like to set a reward for this bounty? (Type 'no' to skip)")
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

        # Request supervisor from user if toggled on
        toggle_supervisor = await self.config.guild(ctx.guild).toggle_supervisor()
        if toggle_supervisor:
            supervisor = None  # Assign None as the default value
            supervisor_msg = await ctx.send("Would you like to assign a supervisor for this bounty? (Type 'yes' or 'no')")
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

                        # Ask if the user should be rewarded with a star
                        star_msg = await ctx.send(f"Should {ctx.author.mention} be rewarded with a star for completing this bounty? (Type 'yes' or 'no')")
                        star_response = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)

                        if star_response.content.lower() == "yes":
                            self.add_star(ctx.author)
                            await ctx.send(f"{ctx.author.mention} has been rewarded with a star!")
                        else:
                            await ctx.send(f"{ctx.author.mention} was not rewarded with a star.")

                        await star_msg.delete()
                        await star_response.delete()

                        await bounty.poster.send(f"Your bounty '{bounty.name}' has been completed by {ctx.author.mention}.")
                    else:
                        await ctx.send("Only the bounty poster or a supervisor can complete a bounty.")
                    return

        await ctx.send("Bounty not found!")

    @bounty_group.command(name="board")
    async def bounty_board(self, ctx):
        await self.send_bounty_board(ctx.guild, ctx.channel)

    @bounty_group.command(name="take")
    async def take_bounty_command(self, ctx, bounty_name):
        for bounty in self.bounties:
            if bounty.name.lower() == bounty_name.lower():
                if not bounty.taken:
                    await self.take_bounty(ctx, bounty)
                else:
                    await ctx.send("This bounty has already been taken.")
                return

        await ctx.send("Bounty not found!")

    def add_star(self, user):
        if user.id not in self.stars:
            self.stars[user.id] = 0
        self.stars[user.id] += 1

    def remove_star(self, user):
        if user.id in self.stars:
            self.stars[user.id] -= 1
            if self.stars[user.id] <= 0:
                del self.stars[user.id]

    @bounty_group.command(name="stars")
    async def user_stars(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        star_count = self.stars.get(user.id, 0)
        await ctx.send(f"{user.mention} has {star_count} stars.")

    @bounty_group.command(name="addstar")
    @checks.is_owner()
    async def add_star_command(self, ctx, user: discord.Member):
        self.add_star(user)
        await ctx.send(f"{user.mention} has been rewarded with a star!")

    @bounty_group.command(name="removestar")
    @checks.is_owner()
    async def remove_star_command(self, ctx, user: discord.Member):
        self.remove_star(user)
        await ctx.send(f"A star has been removed from {user.mention}.")

    @commands.group(name="bountyset")
    @checks.admin_or_permissions(manage_guild=True)
    async def bountyset_group(self, ctx):
        """Manage bounty settings"""
        pass

    @bountyset_group.command(name="supervisor")
    async def set_supervisor_role(self, ctx, role: discord.Role):
        """Set the supervisor role for bounties"""
        await self.config.guild(ctx.guild).supervisor_role.set(role.id)
        await ctx.send(f"The supervisor role for bounties has been set to {role.name}.")

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            bounty_channel_id = await self.config.guild(guild).bounty_channel()
            if bounty_channel_id:
                bounty_channel = guild.get_channel(bounty_channel_id)
                if bounty_channel:
                    await self.send_bounty_board(guild, bounty_channel)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send("You don't have permission to use this command.")

# Setup function for Red
def setup(bot):
    bot.add_cog(BountyBoard(bot))
