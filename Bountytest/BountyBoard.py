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

# Example BountyBoard cog
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
            supervisor_response = await self.bot.wait_for("message", check=lambda m.author == ctx.author and m.channel == ctx.channel)

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

    @bounty_group.command(name="take")
    async def take_bounty(self, ctx, bounty_name):
        for bounty in self.bounties:
            if bounty.name.lower() == bounty_name.lower():
                if not bounty.taken:
                    bounty.taken = True
                    bounty.taken_by = ctx.author
                    await ctx.send(f"Bounty '{bounty.name}' has been taken by {ctx.author.mention}.")

                    await bounty.poster.send(f"Your bounty '{bounty.name}' has been taken by {ctx.author.mention}. Please contact them for further details.")

                    # Set status on the bounty board to pending with emojis
                    bounty_embed = await self.get_bounty_embed(bounty)
                    bounty_embed.set_field_at(0, name=bounty_embed.fields[0].name, value=":hourglass_flowing_sand: Pending", inline=False)
                    await self.update_bounty_board(ctx.guild, ctx.channel, bounty_embed)
                else:
                    await ctx.send("This bounty has already been taken.")
                return

        await ctx.send("Bounty not found!")

    @bounty_group.command(name="board")
    async def bounty_board(self, ctx):
        await self.send_bounty_board(ctx.guild, ctx.channel)

    @bounty_group.command(name="stars")
    async def bounty_stars(self, ctx):
        user_id = str(ctx.author.id)
        star_count = self.stars.get(user_id, 0)
        await ctx.send(f"{ctx.author.mention} has {star_count} stars.")

    @bounty_group.command(name="top")
    async def bounty_top_stars(self, ctx):
        sorted_stars = sorted(self.stars.items(), key=lambda x: x[1], reverse=True)

        if not sorted_stars:
            await ctx.send("No stars have been awarded yet.")
            return

        embed = Embed(title="Top Star Counts", description="")

        for idx, (user_id, star_count) in enumerate(sorted_stars[:10]):
            user = ctx.guild.get_member(int(user_id))
            if user:
                embed.add_field(
                    name=f"**{idx + 1}. {user.display_name}**",
                    value=f"Star Count: {star_count}",
                    inline=False
                )

        await ctx.send(embed=embed)

    async def send_bounty_board(self, guild, channel):
        embed = Embed(title="Bounty Board", description="Active bounties")

        for bounty in self.bounties:
            embed.add_field(
                name=bounty.name,
                value=f"Poster: {bounty.poster.mention}\nDescription: {bounty.description}\nReward: {bounty.reward}\nStatus: {'Taken' if bounty.taken else 'Posted'}",
                inline=False
            )

        await channel.send(embed=embed)

    async def get_bounty_embed(self, bounty):
        embed = Embed(title="Bounty Details", description="")

        embed.add_field(
            name=bounty.name,
            value=f"Poster: {bounty.poster.mention}\nDescription: {bounty.description}\nReward: {bounty.reward}\nStatus: {'Taken' if bounty.taken else 'Posted'}",
            inline=False
        )

        return embed

    async def update_bounty_board(self, guild, channel, bounty_embed):
        messages = await channel.history(limit=10).flatten()
        for message in messages:
            if message.author == self.bot.user and message.embeds:
                embed = message.embeds[0]
                if embed.title == "Bounty Board":
                    await message.edit(embed=bounty_embed)
                    return

        # If no existing bounty board message is found, send a new one
        new_message = await channel.send(embed=bounty_embed)
        return new_message


def setup(bot):
    bot.add_cog(BountyBoard(bot))
