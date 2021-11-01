import discord
from discord.ext import commands

class Cheats(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def cheats(self, ctx):
        embed = discord.Embed(
            colour=discord.Colour.blue(),
            title='Here are the current "cheats" which will not break the game:',
            description='\n\n**Fps** - Displays an FPS counter.\n\n**RegnarDet?** - Forces the weather to rain.\n\n**TorsVrede** - Forces the weather to thunderstorm.\n\n**Solkatt** - Forces the weather to sunny.\n\n**Dimfilt** - Forces the weather to fog.\n\n**Väderlek or Vaderlek** - Sets the weather to the default dynamic setting.\n\n**Händelser or Handelser** - Random events are triggered as often as possible.\n\n**Ögonsten or Ogonsten** - Graphics settings not lowered when zooming out.\n\n**GömdaSaker or GomdaSaker** - Unlocks all decorative objects.\n\n**Uppdatera** - Opens the update link for your installation ([shadowtree.se](https://shadowtree-software.se/tr3/lanes3.apk) / [Google Play](https://play.google.com/store/apps/details?id=se.shadowtree.software.trafficbuilder) / [Amazon](https://www.amazon.com/gp/mas/dl/android?p=se.shadowtree.software.trafficbuilder))\n\n**Blindstyre** - Disables vehicles stopping before crashed vehicles.',
            timestamp=ctx.message.created_at
        )
        embed.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar_url)
        await ctx.reply(embed=embed, mention_author=False)

def setup(client):
    client.add_cog(Cheats(client))