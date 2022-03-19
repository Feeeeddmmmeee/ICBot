import discord, intersection, datetime
from discord.ext import commands
from libs import asqlite

class Stats(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def stats(self, ctx, *, user: discord.User = None):
        if not user: user = ctx.author
        # average | total | top stats
        # top maps | 

        embed = discord.Embed(
            timestamp = ctx.message.created_at,
            color = discord.Color.blue()
        )

        embed.set_author(name = user, icon_url = user.avatar_url)

        await ctx.reply(embed = embed, mention_author = False)

def setup(client):
    client.add_cog(Stats(client))