import random
from redbot.core import commands, Config

class Bitches(commands.Cog):
    """Cog that replies with a random number between -5 and 10 or a custom response."""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)
        default_global = {
            "bitches_responses": [
                "Ya got no bitches!",
                "No bitches for you!",
                "Sorry, no bitches here."
            ]
        }
        self.config.register_global(**default_global)

    @commands.command()
    async def bitches(self, ctx, number: int = None):
        """Replies with a random number between -5 and 10 or a custom response."""
        if number is None:
            random_number = random.randint(-5, 10)
            response = await self.get_bitches_response(random_number)
        else:
            response = await self.get_bitches_response(number)

        await ctx.send(response)

    async def get_bitches_response(self, number):
        """Gets a response for the bitches command based on the given number."""
        if number <= 0:
            responses = await self.config.bitches_responses()
            return random.choice(responses)
        else:
            return f"you have: {number} bitches!"

def setup(bot):
    bot.add_cog(Bitches(bot))
