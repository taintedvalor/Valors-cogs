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
            "interval": 0,
            "channel": None,
            "active": False,
            "last_question_time": 0
        }
        
        self.config.register_guild(**default_settings)
        self.question_task = self.bot.loop.create_task(self.random_question())
        
    @commands.group()
    @checks.admin()
    async def activity(self, ctx):
        """Manage server engagement settings."""
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
            await ctx.send(f"This question is already in the database.")
            
    # ... (other command methods remain the same)

    async def random_question(self):
        await self.bot.wait_until_ready()
        while True:
            for guild in self.bot.guilds:
                active = await self.config.guild(guild).active()
                if active:
                    current_time = time.time()
                    last_question_time = await self.config.guild(guild).last_question_time()
                    interval = await self.config.guild(guild).interval()
                    if current_time - last_question_time >= interval * 3600:
                        role_id = await self.config.guild(guild).role()
                        role = guild.get_role(role_id)
                        channel_id = await self.config.guild(guild).channel()
                        channel = guild.get_channel(channel_id)
                        questions = await self.config.guild(guild).questions()
                        if role and channel and questions:
                            question = random.choice(questions)
                            await channel.send(f"{role.mention} {question}")
                            await self.config.guild(guild).last_question_time.set(current_time)
            await asyncio.sleep(60)  # Check every minute

def setup(bot):
    bot.add_cog(Engagement(bot))
