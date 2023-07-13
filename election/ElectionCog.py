import discord
from redbot.core import commands
import random
import asyncio

class ElectionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.participant_emojis = {}  # Store participant IDs and their corresponding emojis
        self.election_channel_id = None
        self.role_to_inherit_id = None
        self.previous_winner = None
        self.election_period = 86400
        self.participants = []

    @commands.Cog.listener()
    async def on_ready(self):
        print("ElectionCog is ready.")

    @commands.group()
    async def election(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @election.command(name="setchannel")
    async def set_election_channel_command(self, ctx, channel: discord.TextChannel):
        self.election_channel_id = channel.id
        await ctx.send(f"Election channel set to {channel.mention}.")

    @election.command(name="setrole")
    async def set_role_to_inherit_command(self, ctx, role: discord.Role):
        self.role_to_inherit_id = role.id
        await ctx.send(f"Role to inherit set to {role.mention}.")

    @election.command(name="setperiod")
    async def set_election_period_command(self, ctx, period: int):
        if period <= 0:
            await ctx.send("Invalid election period. Please provide a positive integer value.")
            return
        self.election_period = period
        await ctx.send(f"Election period set to {period} seconds.")

    @election.command(name="start")
    async def start_election_command(self, ctx):
        if not all([self.election_channel_id, self.role_to_inherit_id]):
            await ctx.send("Please configure all necessary variables before starting the election.")
            return

        election_channel = self.bot.get_channel(self.election_channel_id)
        if election_channel is None:
            await ctx.send("The configured election channel does not exist.")
            return

        await election_channel.purge()

        embed = discord.Embed(title="Election", description="React to the corresponding emoji to vote for a participant.")
        user_list = [ctx.author]
        message = await election_channel.send(embed=embed)

        # Assign unique emoji to each participant
        for participant in self.participants:
            emoji = self.participant_emojis.get(participant.id, "❓")
            await message.add_reaction(emoji)

        await self.bot.wait_for('message', check=lambda m: m.channel == election_channel and m.author == ctx.author)
        await self.process_election_results(message, user_list)

    async def process_election_results(self, message, user_list):
        await message.clear_reactions()

        for reaction in message.reactions:
            async for user in reaction.users():
                if user != self.bot.user and user.id in self.participant_emojis:
                    participant = discord.utils.get(user_list, id=user.id)
                    if participant:
                        user_emoji = self.participant_emojis[user.id]
                        if reaction.emoji == user_emoji:
                            user_list.remove(participant)
                        else:
                            user_list.append(user)

        embed = discord.Embed(title="Election Results", description="Here are the election results:")
        for user in user_list:
            emoji = self.participant_emojis.get(user.id, "❓")
            embed.add_field(name=user.name, value=f"{user.mention} {emoji}", inline=False)

        winners = [user for user in user_list if user_list.count(user) == max(user_list.count(u) for u in user_list)]
        if winners:
            winner = random.choice(winners)
            embed.set_footer(text=f"The winner is {winner.name} with {user_list.count(winner)} votes!")
        else:
            winner = None

        election_channel = self.bot.get_channel(self.election_channel_id)
        await election_channel.send(embed=embed)

        if winner:
            await self.bot.wait_until_ready()
            await self.handle_election_result(winner)

    async def handle_election_result(self, winner):
        election_channel = self.bot.get_channel(self.election_channel_id)
        role_to_inherit = election_channel.guild.get_role(self.role_to_inherit_id)

        if not role_to_inherit:
            await election_channel.send("The role to inherit does not exist.")
            return

        if winner == role_to_inherit:
            await election_channel.send("The role to inherit cannot be the winner.")
            return

        if winner:
            await election_channel.send(f"The winner is {winner.mention}!")

            if self.previous_winner:
                await self.previous_winner.remove_roles(role_to_inherit)
                await election_channel.send(f"{self.previous_winner.mention} no longer holds the role to inherit.")

            await winner.add_roles(role_to_inherit)
            await election_channel.send(f"{winner.mention} has received the role to inherit.")
            await asyncio.sleep(self.election_period)
            await winner.remove_roles(role_to_inherit)
            await election_channel.send(f"{winner.mention} no longer holds the role to inherit.")

            self.previous_winner = winner
        else:
            await election_channel.send("No one received enough votes in the election.")

    @election.command(name="join")
    async def join_election_command(self, ctx, emoji: str):
        if len(emoji) > 1:
            await ctx.send("Invalid emoji. Please provide a single character emoji.")
            return

        if ctx.author not in self.participants:
            self.participants.append(ctx.author)
            self.participant_emojis[ctx.author.id] = emoji
            await ctx.send(f"{ctx.author.mention} has joined the election with the emoji {emoji}.")
        else:
            await ctx.send(f"{ctx.author.mention} is already part of the election.")

    @election.command(name="settings")
    async def settings_command(self, ctx):
        election_channel = self.bot.get_channel(self.election_channel_id)
        role_to_inherit = ctx.guild.get_role(self.role_to_inherit_id)

        embed = discord.Embed(title="Election Settings", color=discord.Color.blue())
        embed.add_field(name="Election Channel", value=election_channel.mention if election_channel else "Not set")
        embed.add_field(name="Role to Inherit", value=role_to_inherit.mention if role_to_inherit else "Not set")
        embed.add_field(name="Election Period", value=f"{self.election_period} seconds")

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(ElectionCog(bot))
