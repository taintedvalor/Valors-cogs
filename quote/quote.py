import discord
from redbot.core import commands, Config

class Quote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=123456789)  # Replace with a unique identifier
        default_guild_settings = {
            'quote_channel_id': None
        }
        self.config.register_guild(**default_guild_settings)

    @commands.Cog.listener()
    async def on_message(self, message):
        quote_channel_id = await self.config.guild(message.guild).quote_channel_id()

        if quote_channel_id is None:
            return  # Ignore messages if quote channel is not set for the guild

        if message.channel.id == quote_channel_id:
            return  # Ignore messages sent in the quote channel itself

        if message.content.startswith('!quote'):
            link = message.content.split()[1]  # Get the message link from the command
            quote_channel = self.bot.get_channel(quote_channel_id)

            if quote_channel:
                try:
                    quoted_message = await commands.MessageConverter().convert(message, link)
                    embed = self.create_quote_embed(quoted_message)
                    await quote_channel.send(embed=embed)
                    await message.channel.send('Message quoted successfully!')
                except commands.BadArgument:
                    await message.channel.send('Invalid message link!')
            else:
                await message.channel.send('Quote channel not found!')

    def create_quote_embed(self, message):
        embed = discord.Embed(
            title='Quoted Message',
            description=message.content,
            color=discord.Color.blue()
        )
        embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
        embed.add_field(name='Message Link', value=f'[Jump to Message]({message.jump_url})')
        embed.set_footer(text=f'Quoted from #{message.channel.name}')
        return embed

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def setquotechannel(self, ctx, channel: discord.TextChannel):
        await self.config.guild(ctx.guild).quote_channel_id.set(channel.id)
        await ctx.send(f'Quote channel set to #{channel.name}!')

def setup(bot):
    bot.add_cog(Quote(bot))
