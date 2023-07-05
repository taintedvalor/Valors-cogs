import asyncio
from discord import Embed, Message
from redbot.core import commands, Config, checks

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


class BountyBoard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)
        default_guild_config = {
            "supervisor_role": None,
            "toggle_reward": True,
            "toggle_supervisor": True
        }
        self.config.register_guild(**default_guild_config)
        self.bounties = []
        self.stars = {}  # Dictionary to store star counts

        # Start the bounty board update loop
        self.bot.loop.create_task(self.update_bounty_board())

    async def update_bounty_board(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            await self.update_board_messages()
            await asyncio.sleep(5)  # Update every 5 seconds

    async def update_board_messages(self):
        for guild in self.bot.guilds:
            for bounty_channel in guild.text_channels:
                await self.send_bounty_board(guild, bounty_channel)
                break

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

        # Request supervisor from user if toggled on
        toggle_supervisor = await self.config.guild(ctx.guild).toggle_supervisor()
        if toggle_supervisor:
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

        # Update bounty board after creating a new bounty
        await self.update_board_messages()

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
                else:
                    await ctx.send("The bounty has already been marked as completed.")
                return

        await ctx.send(f"No bounty with the name '{bounty_name}' found.")

    @bounty_group.command(name="take")
    async def take_bounty(self, ctx, bounty_name):
        for bounty in self.bounties:
            if bounty.name.lower() == bounty_name.lower():
                if not bounty.taken:
                    bounty.taken = True
                    bounty.taken_by = ctx.author
                    await ctx.send(f"{ctx.author.mention} has taken the bounty '{bounty.name}'.")
                    await bounty.poster.send(f"{ctx.author.mention} has taken your bounty '{bounty.name}'.")
                else:
                    await ctx.send("The bounty has already been taken.")
                return

        await ctx.send(f"No available bounty with the name '{bounty_name}' found.")

    @bounty_group.command(name="stars")
    async def view_stars(self, ctx):
        stars = self.stars.get(ctx.author.id, 0)
        await ctx.send(f"{ctx.author.mention} has {stars} star(s).")

    def add_star(self, user):
        user_id = user.id
        if user_id in self.stars:
            self.stars[user_id] += 1
        else:
            self.stars[user_id] = 1


def setup(bot):
    bot.add_cog(BountyBoard(bot))
