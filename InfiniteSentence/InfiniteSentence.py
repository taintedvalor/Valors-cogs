import discord
from redbot.core import commands, Config

class InfiniteSentence(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)  # Use a unique identifier
        default_guild_settings = {
            "sentence_channel_id": None,
            "last_user_id": None,
            "sentence": []
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

            last_user_id = await self.config.guild(message.guild).last_user_id()
            if last_user_id == message.author.id:
                return  # Skip if the same user has sent a word before

            if word:
                sentence = await self.get_sentence(message.guild)
                sentence.append(word)
                await self.config.guild(message.guild).sentence.set(sentence)
                await self.config.guild(message.guild).last_user_id.set(message.author.id)
                await self.update_sentence_embed(message.guild)

    async def update_sentence_embed(self, guild):
        channel_id = await self.config.guild(guild).sentence_channel_id()
        channel = self.bot.get_channel(channel_id)
        if channel is None:
            return

        sentence = await self.get_sentence(guild)

        embed = discord.Embed(title="Infinite Sentence", color=discord.Color.blue())
        embed.description = " ".join(sentence)

        await channel.purge(limit=None, check=lambda m: m.author == self.bot.user)
        await channel.send(embed=embed)

    async def get_sentence(self, guild):
        return await self.config.guild(guild).sentence()

    @commands.group(name="sentence", invoke_without_command=True)
    @commands.guild_only()
    @commands.admin()
    async def sentence_group(self, ctx):
        """
        Manage the infinite sentence.
        """
        await ctx.send_help(ctx.command)

    @sentence_group.command(name="setchannel")
    async def set_sentence_channel(self, ctx, channel: discord.TextChannel):
        """
        Sets the channel for the infinite sentence.
        """
        await self.config.guild(ctx.guild).sentence_channel_id.set(channel.id)
        await ctx.send(f"The infinite sentence channel has been set to {channel.mention}.")
        await self.update_sentence_embed(ctx.guild)

    @sentence_group.command(name="reset")
    async def reset_sentence(self, ctx):
        """
        Resets the infinite sentence.
        """
        await self.config.guild(ctx.guild).sentence.set([])
        await self.config.guild(ctx.guild).last_user_id.set(None)
        await self.update_sentence_embed(ctx.guild)
        await ctx.send("The infinite sentence has been reset.")

def setup(bot):
    bot.add_cog(InfiniteSentence(bot))
