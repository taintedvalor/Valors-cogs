import discord
from redbot.core import commands, Config
import random

class Womp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)  # Replace with your own unique identifier
        default_guild_settings = {"toggle": False}
        self.config.register_guild(**default_guild_settings)

    @commands.group(name='womp')
    async def womp_group(self, ctx):
        """Manage the womp response."""
        pass

    @womp_group.command(name='toggle')
    async def toggle_womp(self, ctx):
        """Toggle the womp response on/off."""
        current_state = await self.config.guild(ctx.guild).toggle()
        await self.config.guild(ctx.guild).toggle.set(not current_state)
        await ctx.send(f"Womp response is now {'enabled' if not current_state else 'disabled'}.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        guild_settings = await self.config.guild(message.guild).all()
        if guild_settings["toggle"] and "womp" in message.content.lower():
            num_womps = message.content.lower().count("womp")
            min_amount = num_womps
            max_amount = num_womps + 2  # Adjust as needed
            random_amount = random.randint(min_amount, max_amount)
            
            womp_effect = ''.join([
                f"**{char}**" if char == "womp" else char
                for char in " womp" * random_amount
            ])

            # Extract emojis from the original message
            emojis = [str(emoji) for emoji in message.content.split() if emoji.isnumeric() or emoji in discord.emojis]

            # Add random emojis or include original emojis in the response
            if random.choice([True, False]):  # Adjust the probability as needed
                random_emojis = [random.choice(self.bot.emojis) for _ in range(random.randint(1, 3))]
                response = f"{womp_effect} {' '.join(random_emojis)}"
            elif emojis:
                response = f"{womp_effect} {' '.join(emojis)}"
            else:
                response = womp_effect

            if "~" in message.content:
                punctuation = "~"
            else:
                punctuation = random.choice(['.', '!', '?'])
                
            capitalized_womp_effect = ' '.join([
                word.capitalize() if i % 2 == 0 else word
                for i, word in enumerate(response.split())
            ])
            
            response = f"{capitalized_womp_effect}{punctuation}"
            
            await message.channel.send(response)

def setup(bot):
    bot.add_cog(Womp(bot))
