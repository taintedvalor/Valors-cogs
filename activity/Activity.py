import discord
from redbot.core import commands, Config, checks, embeds

class Activity(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)  # Change this identifier
        default_settings = {
            "questions": [],
            "interval": 24,  # Default interval in hours
            "role": None,
            "channel": None,
            "active": False
        }
        self.config.register_guild(**default_settings)

    @commands.group()
    async def activity(self, ctx):
        """Manage the Activity cog settings."""
        pass
    
    @activity.command()
    async def add(self, ctx, *, question: str):
        """Add a question to the list."""
        questions = await self.config.guild(ctx.guild).questions()
        questions.append(question)
        await self.config.guild(ctx.guild).questions.set(questions)
        await ctx.send(f"Question added: {question}")
    
    @activity.command()
    async def remove(self, ctx, *, question: str):
        """Remove a question from the list."""
        questions = await self.config.guild(ctx.guild).questions()
        if question in questions:
            questions.remove(question)
            await self.config.guild(ctx.guild).questions.set(questions)
            await ctx.send(f"Question removed: {question}")
        else:
            await ctx.send("Question not found.")
    
    @activity.command()
    async def settings(self, ctx):
        """View cog settings."""
        settings = await self.config.guild(ctx.guild).all()
        
        embed = embeds.Embed(title="Activity Cog Settings", color=discord.Color.blue())
        embed.add_field(name="Interval", value=f"{settings['interval']} hours")
        
        role_id = settings["role"]
        role = ctx.guild.get_role(role_id)
        embed.add_field(name="Ping Role", value=role.mention if role else "Not set")
        
        channel_id = settings["channel"]
        channel = ctx.guild.get_channel(channel_id)
        embed.add_field(name="Question Channel", value=channel.mention if channel else "Not set")
        
        questions = settings["questions"]
        if questions:
            questions_str = "\n".join(questions)
            embed.add_field(name="Questions", value=questions_str)
        else:
            embed.add_field(name="Questions", value="No questions")
        
        active = settings["active"]
        embed.add_field(name="Active", value="Yes" if active else "No")
        
        await ctx.send(embed=embed)
    
    @activity.command()
    async def interval(self, ctx, hours: int):
        """Set the question interval."""
        await self.config.guild(ctx.guild).interval.set(hours)
        await ctx.send(f"Question interval set to {hours} hours.")
    
    @activity.command()
    async def role(self, ctx, role: discord.Role):
        """Set the role to ping."""
        await self.config.guild(ctx.guild).role.set(role.id)
        await ctx.send(f"Ping role set to {role.name}.")
    
    @activity.command()
    async def channel(self, ctx, channel: discord.TextChannel):
        """Set the question channel."""
        await self.config.guild(ctx.guild).channel.set(channel.id)
        await ctx.send(f"Question channel set to {channel.mention}.")
    
    @activity.command()
    async def start(self, ctx):
        """Start sending questions."""
        await self.config.guild(ctx.guild).active.set(True)
        # Start a loop to send questions at the specified interval
    
    @activity.command()
    async def stop(self, ctx):
        """Stop sending questions."""
        await self.config.guild(ctx.guild).active.set(False)
        # Stop the loop that sends questions

def setup(bot):
    bot.add_cog(Activity(bot))
