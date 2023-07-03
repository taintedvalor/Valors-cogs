import discord
from redbot.core import commands, Config

class InfiniteSentence(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)  # Use a unique identifier
        default_guild_settings = {
            "sentence_channel_id": None
        }
        self.config.register_guild(**default_guild_settings)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        channel_id = await self.config.guild(message.guild).sentence_channel_id()
        if channel_id is not None and message.channel.id == channel_id:
            word = message.content.strip()
            await message.delete()

            if word:
                sentence = await self.get_sentence(message.guild)
                sentence.append(word)
                await self.update_sentence_embed(message.guild)

    async def update_sentence_embed(self, guild):
        channel_id = await self.config.guild(guild).sentence_channel_id()
        channel = self.bot.get_channel(channel_id)
        if channel is None:
            return

        sentence = await self.get_sentence(guild)

        embed = discord.Embed(title="Infinite Sentence", color=discord.Color.blue())
        embed.description = " ".join(sentence)

        async for msg in channel.history(limit=1):
            if msg.author == self.bot.user:
                await msg.delete()

        await channel.send(embed=embed)

    async def get_sentence(self, guild):
        return await self.config.guild(guild).sentence()

    @commands.group()
    @commands.guild_only()
    @commands.admin()
    async def sentence(self, ctx):
        """Manage the infinite sentence."""
        pass

    @sentence.command(name="setchannel")
    async def set_sentence_channel(self, ctx, channel: discord.TextChannel):
        """Sets the channel for the infinite sentence."""
        await self.config.guild(ctx.guild).sentence_channel_id.set(channel.id)
        await ctx.send(f"The infinite sentence channel has been set to {channel.mention}.")

    @sentence.command(name="reset")
    async def reset_sentence(self, ctx):
        """Resets the infinite sentence."""
        await self.config.guild(ctx.guild).sentence.set([])
        await self.update_sentence_embed(ctx.guild)
        await ctx.send("The infinite sentence has been reset.")

def setup(bot):
    bot.add_cog(InfiniteSentence(bot))
