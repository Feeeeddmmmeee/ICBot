import discord
from discord.ext import commands

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
            title = "Available Commands",
            description = "No, you can't get detailed help information on each\n command because I was to lazy to make that so don't \nattempt to run `ic help command`.",
            color = discord.Color.blue()
        )

        embed.add_field(name="Admin / Developer", value="`ic link` `ic unlink` `ic debug` `ic bypass`", inline=False)
        embed.add_field(name="Profiles and Stuff", value="`ic profile` `ic verify` `ic map` `ic search`", inline=False)
        embed.add_field(name="Other", value="`ic cheats` `ic rules` `ic suggest` `ic help` `ic ping`", inline=False)


        await ctx.reply(embed = embed, mention_author=False)

def setup(client):
    client.add_cog(Help(client))