import discord, json
from discord.ext import commands

class Suggest(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def suggest(self, ctx, *, suggestion):
        with open("config/validguilds.json", "r") as config:
            validated  = ctx.guild.id in json.load(config)

        if not validated:
            embed = discord.Embed(
                description = f"<:neutral:905485648478228490> This command isn't available in your server!",
                color = discord.Color.blue()
            )

            await ctx.reply(embed=embed, mention_author=False)
            return

        embed = discord.Embed(
                colour=discord.Colour.from_rgb(66, 135, 245),
                timestamp=ctx.message.created_at,
                description=suggestion,
            )
        embed.set_footer(text=f"Suggested by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

        if len(ctx.message.attachments):
            attachment = ctx.message.attachments[0]
            embed.set_image(url = attachment.url)

        channel = ctx.bot.get_channel(600465489508171776)#600465489508171776
        like = self.client.get_emoji(759059895424909380)
        dislike = self.client.get_emoji(759060520455766036)

        likes = await channel.send(embed=embed)

        await ctx.message.add_reaction('📬')
        await likes.add_reaction(like)
        await likes.add_reaction(dislike)
        await likes.add_reaction('🤍')

def setup(client):
    client.add_cog(Suggest(client))