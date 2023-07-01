import discord
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS

class TruthOrDareCog(commands.Cog):
    def __init__(self, bot: Red):
        self.bot = bot

    @commands.command()
    async def truth_or_dare(self, ctx: commands.Context):
        buttons = [
            {"name": "Truth", "emoji": "\U0001F4AC", "style": discord.ButtonStyle.primary, "id": "truth"},
            {"name": "Dare", "emoji": "\U0001F64C", "style": discord.ButtonStyle.primary, "id": "dare"},
            {"name": "NSFW", "emoji": "\U0001F51E", "style": discord.ButtonStyle.danger, "id": "nsfw"}
        ]

        async def menu_callback(interaction: discord.Interaction, page: dict, controls: dict):
            button_id = interaction.component.custom_id

            if button_id == "truth":
                await interaction.response.send_message("You clicked the Truth button!")
            elif button_id == "dare":
                await interaction.response.send_message("You clicked the Dare button!")
            elif button_id == "nsfw":
                await interaction.response.send_message("You clicked the NSFW button!")

        await menu(ctx, pages=[{}], controls=DEFAULT_CONTROLS, message=None, button_list=buttons, menu_callback=menu_callback)

@commands.is_owner()
@commands.group()
async def truthdare(ctx: commands.Context):
    """Truth or Dare game commands."""
    pass

@truthdare.command()
async def play(ctx: commands.Context):
    """Starts a Truth or Dare game."""
    await ctx.invoke(self.bot.get_command("truth_or_dare"))

def setup(bot: Red):
    cog = TruthOrDareCog(bot)
    bot.add_cog(cog)
