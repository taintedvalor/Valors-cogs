from .venting import Venting

def setup(bot):
    bot.add_cog(Venting(bot))
