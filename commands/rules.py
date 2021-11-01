import discord, json
from discord.ext import commands

class Rules(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ["rule"])
    async def rules(self, ctx, number):
        with open("config/rules.json", "r") as f:
            file = json.load(f)
            
        embed = discord.Embed(
            colour = discord.Colour.from_rgb(66, 135, 245),
            title = file[number]["title"],
            description = file[number]["desc"]
        )

        await ctx.reply(embed=embed, mention_author=False)

def setup(client):
    client.add_cog(Rules(client))