import discord
from redbot.core import commands
import random
import asyncio

class Election(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.elections = {}  # Dictionary to store ongoing elections

    @commands.command()
    async def election(self, ctx, role: discord.Role, duration: int, channel: discord.TextChannel):
        """Create an election for a specific role."""
        guild_id = ctx.guild.id

        if guild_id in self.elections:
            await ctx.send("An election is already in progress.")
            return

        embed = discord.Embed(
            title="Election Board",
            description=f"React with the corresponding emoji to vote for a participant.",
            color=discord.Color.red()
        )

        embed.add_field(name="Role", value=role.mention, inline=False)
        embed.add_field(name="Duration", value=f"{duration} seconds", inline=False)
        embed.set_footer(text=f"Election initiated by {ctx.author.display_name}")

        message = await channel.send(embed=embed)

        self.elections[guild_id] = {
            'role': role,
            'duration': duration,
            'channel': channel,
            'message': message.id,
            'candidates': {}
        }

        await message.add_reaction("✅")  # Reaction to be used for voting

        await ctx.send(f"Election created for role {role.name}. Voting board has been set in {channel.mention}.")

        await self.election_timer(guild_id)

    async def election_timer(self, guild_id):
        await asyncio.sleep(self.elections[guild_id]['duration'])
        if guild_id in self.elections:
            await self.declare_winner(guild_id)

    async def declare_winner(self, guild_id):
        guild = self.bot.get_guild(guild_id)
        election = self.elections[guild_id]

        if not election['candidates']:
            await election['channel'].send("No participants in the election.")
            return

        winner_id = max(election['candidates'], key=lambda x: election['candidates'][x]['votes'])
        role = election['role']

        winner_member = guild.get_member(winner_id)

        if winner_member is None:
            await election['channel'].send("The winner is no longer a member of the server.")
            return

        await winner_member.add_roles(role, reason="Winner of the election")

        remove_role = True  # Set to True if all non-winners should be removed from the role

        if remove_role:
            for candidate_id in election['candidates']:
                if candidate_id != winner_id:
                    candidate_member = guild.get_member(candidate_id)
                    if candidate_member is not None:
                        await candidate_member.remove_roles(role)

        embed = discord.Embed(
            title="Election Board",
            description=f"The winner of the election is {winner_member.display_name}!",
            color=discord.Color.green()
        )

        embed.add_field(name="Role", value=role.mention, inline=False)
        embed.add_field(name="Duration", value=f"{election['duration']} seconds", inline=False)

        message = await election['channel'].fetch_message(election['message'])
        await message.edit(embed=embed)

        del self.elections[guild_id]

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if not payload.member.bot:
            guild_id = payload.guild_id
            election = self.elections.get(guild_id)

            if election is None:
                return

            channel = self.bot.get_channel(payload.channel_id)

            if channel is None or channel.id != election['channel'].id:
                return

            message = await channel.fetch_message(payload.message_id)

            if message.id != election['message']:
                return

            reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)

            if reaction is not None and reaction.count > 1:
                candidate_id = str(payload.user_id)

                if candidate_id not in election['candidates']:
                    election['candidates'][candidate_id] = {
                        'votes': reaction.count - 1,
                        'emoji': str(payload.emoji)
                    }
                else:
                    election['candidates'][candidate_id]['votes'] = reaction.count - 1

    @commands.command()
    async def election_status(self, ctx):
        """Display the current status of the ongoing election."""
        guild_id = ctx.guild.id

        if guild_id not in self.elections:
            await ctx.send("There is no ongoing election.")
            return

        election = self.elections[guild_id]

        embed = discord.Embed(
            title="Election Status",
            description="Current status of the ongoing election.",
            color=discord.Color.blue()
        )

        embed.add_field(name="Role", value=election['role'].mention, inline=False)
        embed.add_field(name="Duration", value=f"{election['duration']} seconds", inline=False)
        embed.add_field(name="Participants", value=len(election['candidates']), inline=False)

        if election['candidates']:
            candidates_info = '\n'.join([
                f"{election['candidates'][c]['emoji']} - {ctx.guild.get_member(int(c)).mention}"
                for c in election['candidates']
            ])
            embed.add_field(name="Participants List", value=candidates_info, inline=False)

        message = await election['channel'].fetch_message(election['message'])
        await message.edit(embed=embed)

    @commands.command()
    async def cancel_election(self, ctx):
        """Cancel the ongoing election."""
        guild_id = ctx.guild.id

        if guild_id not in self.elections:
            await ctx.send("There is no ongoing election.")
            return

        del self.elections[guild_id]
        await ctx.send("The ongoing election has been canceled.")

def setup(bot):
    bot.add_cog(Election(bot))
