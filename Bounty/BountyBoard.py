from discord import Embed, Message
from redbot.core import commands, Config, checks

# Example Bounty class
class Bounty:
    def __init__(self, name, description, reward):
        self.name = name
        self.description = description
        self.reward = reward
        self.poster = None
        self.taken = False
        self.completed = False

# Example BountyBoard cog
class BountyBoard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)
        default_guild_config = {
            "supervisor_role": None
        }
        self.config.register_guild(**default_guild_config)
        self.bounties = []
        self.bounty_channels = {}  # guild_id: role_id

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
        supervisor_msg: Message = await ctx.send("Would you like a supervisor assigned to moderate the agreement? (Type 'yes' or 'no')")
        supervisor_response = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)

        if supervisor_response.content.lower() == "yes":
            supervisor = ctx.author
            await supervisor_msg.delete()
        else:
            supervisor = None

        await supervisor_response.delete()

        bounty = Bounty(name, description, reward)
        bounty.poster = ctx.author

        self.bounties.append(bounty)

        # Notify the poster
        await ctx.send(f"**Bounty created!**\nName: {name}\nDescription: {description}\nReward: {reward}")

        # Notify the supervisor
        supervisor_role_id = await self.config.guild(ctx.guild).supervisor_role()
        if supervisor_role_id and supervisor:
            supervisor_role = ctx.guild.get_role(supervisor_role_id)
            if supervisor_role:
                await supervisor_role.send(f"A new bounty '{bounty.name}' requires your supervision.")

    @bounty_group.command(name="take")
    async def take_bounty(self, ctx, bounty_name):
        for bounty in self.bounties:
            if bounty.name.lower() == bounty_name.lower():
                if bounty.taken:
                    await ctx.send("This bounty has already been taken!")
                    return

                bounty.taken = True

                # Notify the poster
                poster = bounty.poster
                if poster:
                    await poster.send(f"Your bounty '{bounty.name}' has been taken by {ctx.author.display_name}!")

                return

        await ctx.send("Bounty not found!")

    @bounty_group.command(name="complete")
    async def complete_bounty(self, ctx, bounty_name):
        for bounty in self.bounties:
            if bounty.name.lower() == bounty_name.lower():
                if not bounty.taken:
                    await ctx.send("This bounty hasn't been taken yet!")
                    return

                if bounty.completed:
                    await ctx.send("This bounty has already been completed!")
                    return

                bounty.completed = True

                # Remove bounty from the board
                self.bounties.remove(bounty)

                # Notify the poster
                poster = bounty.poster
                if poster:
                    await poster.send(f"Congratulations! Your bounty '{bounty.name}' has been completed!")

                return

        await ctx.send("Bounty not found!")

    @bounty_group.command(name="board")
    async def bounty_board(self, ctx):
        if not self.bounties:
            await ctx.send("There are no active bounties.")
            return

        embed = Embed(title="Bounty Board", description="Current Bounties")

        for idx, bounty in enumerate(self.bounties):
            status_emoji = "⏳" if bounty.taken else "❌"
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

    @commands.Cog.listener()
    async def on_ready(self):
        print("BountyBoard cog loaded.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.channel, commands.DMChannel) and not message.author.bot:
            for bounty in self.bounties:
                if bounty.poster == message.author:
                    if not bounty.taken:
                        await message.author.send(f"Your bounty '{bounty.name}' has not been taken yet.")
                    elif not bounty.completed:
                        await message.author.send(f"Your bounty '{bounty.name}' has been taken but not completed yet.")
                    break

# Bot setup
def setup(bot):
    bot.add_cog(BountyBoard(bot))
