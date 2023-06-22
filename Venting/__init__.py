from .venting import Venting

def setup(bot):
    cog = Venting(bot)
    bot.add_cog(cog)
