from discord.ext import commands
from redbot.core import commands, Config, bank
from redbot.core.bot import Red
from redbot.core.utils import menus
from discord.ui import Button, View

class TruthOrDare(commands.Cog):
    def __init__(self, bot: Red):
        self.bot = bot

    @commands.command()
    async def truth_or_dare(self, ctx: commands.Context):
        buttons = [
            Button(style=ButtonStyle.primary, label="Truth", custom_id="truth"),
            Button(style=ButtonStyle.primary, label="Dare", custom_id="dare"),
            Button(style=ButtonStyle.danger, label="NSFW", custom_id="nsfw")
        ]

        view = TruthOrDareView()
        view.add_item(*buttons)

        await ctx.send("Choose an option:", view=view)

class TruthOrDareView(View):
    @button.custom_id("truth")
    async def truth_button(self, button: Button, interaction: Interaction):
        await interaction.response.send_message("You clicked the Truth button!")

    @button.custom_id("dare")
    async def dare_button(self, button: Button, interaction: Interaction):
        await interaction.response.send_message("You clicked the Dare button!")

    @button.custom_id("nsfw")
    async def nsfw_button(self, button: Button, interaction: Interaction):
        await interaction.response.send_message("You clicked the NSFW button!")

def setup(bot):
    bot.add_cog(TruthOrDare(bot))
