import discord
import random
from redbot.core import commands, Config, checks, bot

class Activity(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)  # Change the identifier
        default_guild = {
            "questions": [],      # List of questions
            "interval": 2,        # Default interval in hours
            "role": None,         # Role to ping
            "activity_channel": None  # Channel for activity messages
        }
        self.config.register_guild(**default_guild)
        self.task = self.bot.loop.create_task(self.ask_question_loop())

    async def ask_question_loop(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            await self.ask_question_all_guilds()
            interval = await self.config.interval()
            await discord.utils.sleep_until(self.bot.loop, discord.Object(id=0).created_at.timestamp() + (interval * 3600))

    @commands.group(name="activity", aliases=["act"])
    async def activity(self, ctx):
        """Manage the Activity cog."""
        pass

    @activity.command(name="setup")
    async def setup(self, ctx):
        """Guided setup instructions."""
        pass

    @activity.command(name="add")
    async def add(self, ctx, *, question: str):
        """Add a new question to the database."""
        questions = await self.config.questions()
        if question not in questions:
            questions.append(question)
            await self.config.questions.set(questions)
            await ctx.send(f"Added question: {question}")
        else:
            await ctx.send("Question already exists.")

    @activity.command(name="remove")
    async def remove(self, ctx, *, question: str):
        """Remove a question from the database."""
        questions = await self.config.questions()
        if question in questions:
            questions.remove(question)
            await self.config.questions.set(questions)
            await ctx.send(f"Removed question: {question}")
        else:
            await ctx.send("Question not found.")

    @activity.command(name="list")
    async def list_questions(self, ctx):
        """List all available questions."""
        questions = await self.config.questions()
        if questions:
            embed = discord.Embed(title="List of Questions", color=discord.Color.blue())
            for idx, question in enumerate(questions, start=1):
                embed.add_field(name=f"Question {idx}", value=question, inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("No questions available.")

    @activity.command(name="interval")
    async def set_interval(self, ctx, hours: int):
        """Set the time interval for asking questions."""
        if hours > 0:
            await self.config.interval.set(hours)
            await ctx.send(f"Question interval set to {hours} hours.")
        else:
            await ctx.send("Interval must be a positive number.")

    @activity.command(name="role")
    async def set_role(self, ctx, role: discord.Role):
        """Set the role to ping when asking questions."""
        await self.config.role.set(role.id)
        await ctx.send(f"Question role set to {role.mention}.")

    @activity.command(name="setchannel")
    async def set_channel(self, ctx, channel: discord.TextChannel = None):
        """Set the channel for activity messages."""
        if not channel:
            await self.config.activity_channel.set(None)
            await ctx.send("Activity channel has been cleared.")
        else:
            await self.config.activity_channel.set(channel.id)
            await ctx.send(f"Activity messages will be sent in {channel.mention}.")

    @activity.command(name="start")
    async def start_activity(self, ctx):
        """Start asking questions at the configured interval."""
        await self.config.role.set(ctx.author.id)
        await ctx.send("Activity started.")

    @activity.command(name="stop")
    async def stop_activity(self, ctx):
        """Stop asking questions."""
        await self.config.role.set(None)
        await ctx.send("Activity stopped.")

    async def ask_question_all_guilds(self):
        for guild in self.bot.guilds:
            await self.ask_question(guild)

    async def ask_question(self, guild):
        questions = await self.config.questions()
        if questions:
            role_id = await self.config.role()
            if role_id:
                role = guild.get_role(role_id)
                if role:
                    channel_id = await self.config.activity_channel()
                    if channel_id:
                        channel = guild.get_channel(channel_id)
                        if channel:
                            question = random.choice(questions)
                            embed = discord.Embed(title="Random Question", description=question, color=discord.Color.green())
                            await channel.send(embed=embed)

    async def cog_check(self, ctx):
        """Check if the cog is properly set up."""
        return await self.config.role() is not None

    async def get_role_mention(self, guild):
        role_id = await self.config.role()
        if role_id:
            role = guild.get_role(role_id)
            if role:
                return role.mention
        return "No role set."

def setup(bot):
    bot.add_cog(Activity(bot))
