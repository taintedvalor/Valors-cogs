import discord
from redbot.core import commands, Config, checks
import random
import asyncio

class Engagement(commands.Cog):
    """Server engagement with random questions."""
    
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)
        
        default_settings = {
            "questions": [],
            "role": None,
            "interval": 3,  # Default interval is 3 hours
            "channel": None,
            "active": False,
            "embed_active": False,
            "embed_color": None
        }
        
        self.config.register_guild(**default_settings)
        self.question_task = self.bot.loop.create_task(self.random_question())
        
    @commands.group()
    @checks.admin()
    async def activity(self, ctx):
        """Manage server engagement settings."""
        pass
    
    @activity.group(name="embed")
    async def activity_embed(self, ctx):
        """Customize and toggle question embeds."""
        pass
    
    @activity.command(name="add")
    async def activity_add(self, ctx, *, question: str):
        """Add a question for server engagement."""
        questions = await self.config.guild(ctx.guild).questions()
        if question not in questions:
            questions.append(question)
            await self.config.guild(ctx.guild).questions.set(questions)
            await ctx.send(f"Added question: {question}")
        else:
            questions.remove(question)
            await self.config.guild(ctx.guild).questions.set(questions)
            await ctx.send(f"Removed question: {question}")
            
    @activity.command(name="role")
    async def activity_role(self, ctx, role: discord.Role):
        """Set the role to be pinged for questions."""
        await self.config.guild(ctx.guild).role.set(role.id)
        await ctx.send(f"Activity role set to: {role.mention}")
        
    @activity.command(name="interval")
    async def activity_interval(self, ctx, hours: int):
        """Set the interval for sending questions (in hours)."""
        await self.config.guild(ctx.guild).interval.set(hours)
        await ctx.send(f"Question interval set to: {hours} hours")
        self.question_task.cancel()
        self.question_task = self.bot.loop.create_task(self.random_question())
        
    @activity.command(name="channel")
    async def activity_channel(self, ctx, channel: discord.TextChannel):
        """Set the channel for sending questions."""
        await self.config.guild(ctx.guild).channel.set(channel.id)
        await ctx.send(f"Question channel set to: {channel.mention}")
        
    @activity.command(name="toggle")
    async def activity_toggle(self, ctx):
        """Toggle sending questions on/off."""
        active = await self.config.guild(ctx.guild).active()
        await self.config.guild(ctx.guild).active.set(not active)
        if not active:
            await ctx.send("Questions are now on")
        else:
            await ctx.send("Questions are now off")
            
    @activity.command(name="settings")
    async def activity_settings(self, ctx, setting: str = None):
        """View or configure activity settings."""
        if setting:
            if setting == "interval":
                interval = await self.config.guild(ctx.guild).interval()
                await ctx.send(f"Current interval: {interval} hours")
            elif setting == "role":
                role_id = await self.config.guild(ctx.guild).role()
                role = ctx.guild.get_role(role_id)
                await ctx.send(f"Current role: {role.mention}")
        else:
            interval = await self.config.guild(ctx.guild).interval()
            role_id = await self.config.guild(ctx.guild).role()
            role = ctx.guild.get_role(role_id)
            questions = await self.config.guild(ctx.guild).questions()
            question_list = "\n".join(questions)
            await ctx.send(f"Current settings:\nInterval: {interval} hours\nRole: {role.mention}\nQuestions:\n{question_list}")
            
    @activity_embed.command(name="toggle")
    async def activity_embed_toggle(self, ctx):
        """Toggle sending question embeds on/off."""
        embed_active = await self.config.guild(ctx.guild).embed_active()
        await self.config.guild(ctx.guild).embed_active.set(not embed_active)
        if not embed_active:
            await ctx.send("Question embeds are now on")
        else:
            await ctx.send("Question embeds are now off")
            
    @activity_embed.command(name="customize")
    async def activity_embed_customize(self, ctx, color: discord.Color = None):
        """Customize the color of question embeds."""
        if color:
            await self.config.guild(ctx.guild).embed_color.set(color.value)
            await ctx.send(f"Embed color customized to: {color}")
        else:
            await self.config.guild(ctx.guild).embed_color.clear()
            await ctx.send("Embed color customization cleared")
            
    async def random_question(self):
        await self.bot.wait_until_ready()
        while True:
            for guild in self.bot.guilds:
                active = await self.config.guild(guild).active()
                embed_active = await self.config.guild(guild).embed_active()
                if active:
                    role_id = await self.config.guild(guild).role()
                    role = guild.get_role(role_id)
                    channel_id = await self.config.guild(guild).channel()
                    channel = guild.get_channel(channel_id)
                    questions = await self.config.guild(guild).questions()
                    if role and channel and questions:
                        question = random.choice(questions)
                        if embed_active:
                            embed_color_value = await self.config.guild(guild).embed_color()
                            embed_color = discord.Color(embed_color_value) if embed_color_value else discord.Color.random()
                            embed = discord.Embed(title="Random Question", description=question, color=embed_color)
                            await channel.send(f"{role.mention}", embed=embed)
                        else:
                            await channel.send(f"{role.mention} {question}")
            interval = await self.config.guild(guild).interval()
            await asyncio.sleep(interval * 3600)

def setup(bot):
    bot.add_cog(Engagement(bot))
