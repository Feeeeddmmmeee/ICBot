import asyncio, io
import discord, intersection
from discord.ext import commands
from matplotlib import pyplot as plt
from libs import asqlite
from collections import Counter
import pandas as pd

async def get_followers(member: discord.Member):
    async with asqlite.connect("database.sqlite") as conn:
        async with conn.cursor() as cursor:

            await cursor.execute(f'SELECT ic_id FROM accounts WHERE discord_id = {member.id}')
            id = await cursor.fetchone()
            
    if id:
        ic_user_object = intersection.user.get_details_for_user(userId=id[0])
        return ic_user_object.followers

class Chart(commands.Cog):

    def __init__(self, client):
        self.client = client

    '''@commands.group(invoke_without_command=True)
    async def chart(self, ctx):
        embed = discord.Embed(
                description = f"<:neutral:905485648478228490> This commands requires an argument that can be set to either **roles** or **all**!",
                color = discord.Color.blue()
            )

        await ctx.reply(embed=embed, mention_author=False)'''

    @commands.command()
    async def chart(self, ctx):
        data_stream = io.BytesIO()
        y = [len(discord.utils.get(ctx.guild.roles,name="Newbie (Below 10 Followers)").members), len(discord.utils.get(ctx.guild.roles,name="10+ Followers").members), len(discord.utils.get(ctx.guild.roles,name="50+ Followers").members), len(discord.utils.get(ctx.guild.roles,name="100+ Followers").members), len(discord.utils.get(ctx.guild.roles, name="200+ Followers").members), len(discord.utils.get(ctx.guild.roles,name="500+ Followers").members), len(discord.utils.get(ctx.guild.roles,name="1000+ Followers").members)]
        x = [0, 10, 50, 100, 200, 500, 1000]

        plt.plot(x,y)

        #await ctx.send(y)

        plt.title("Followers")
        plt.ylabel("Amount of Users")
        plt.xlabel("Follower Thresholds (Roles)")

        plt.savefig(data_stream, format='png', bbox_inches="tight", dpi = 80)
        plt.close()

        data_stream.seek(0)
        chart = discord.File(data_stream,filename="follower_chart.png")

        embed = discord.Embed(timestamp = ctx.message.created_at, color = discord.Color.blue(), title="Follower chart based on Discord roles")
        embed.set_footer(icon_url=ctx.author.avatar_url, text=ctx.author)
        embed.set_image(url="attachment://follower_chart.png")

        await ctx.reply(embed=embed, file=chart, mention_author=False)
'''
    @chart.command()
    async def all(self, ctx):
        data_stream = io.BytesIO()
        task = []
        followers = []

        for member in ctx.guild.members:
            task.append(asyncio.create_task(get_followers(member)))

        for future in task:
            followers.append(await future)

        await ctx.send(followers)

        followers[:] = (value for value in followers if value != None)
        followers = sorted(followers)

        sorted_counted = Counter(followers)

        range_length = list(range(max(followers))) # Get the largest value to get the range.
        data_series = {}

        for i in range_length:
            data_series[i] = 0 # Initialize series so that we have a template and we just have to fill in the values.

        for key, value in sorted_counted.items():
            data_series[key] = value

        data_series = pd.Series(data_series)
        x_values = data_series.index

        # you can customize the limits of the x-axis
        # plt.xlim(0, max(followers))
        plt.bar(x_values, data_series.values, width=3)

        plt.title("Followers")
        plt.ylabel("Amount of Users")
        plt.xlabel("Followers")

        plt.savefig(data_stream, format='png', bbox_inches="tight", dpi = 80)
        plt.close()

        data_stream.seek(0)
        chart = discord.File(data_stream,filename="follower_chart.png")

        embed = discord.Embed(timestamp = ctx.message.created_at, color = discord.Color.blue(), title="Follower chart based on raw follower data")
        embed.set_footer(icon_url=ctx.author.avatar_url, text=ctx.author)
        
        embed.set_image(url="attachment://follower_chart.png")

        await ctx.reply(embed=embed, file=chart, mention_author=False)'''

def setup(client):
    client.add_cog(Chart(client))