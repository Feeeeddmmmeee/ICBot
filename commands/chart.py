import discord, intersection, io
from discord.ext import commands
from matplotlib import pyplot as plt
from libs import asqlite
from collections import Counter


class Chart(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True)
    async def chart(self, ctx):
        embed = discord.Embed(
                description = f"<:neutral:905485648478228490> This commands requires an argument that can be set to either **roles** or **all**!",
                color = discord.Color.blue()
            )

        await ctx.reply(embed=embed, mention_author=False)

    @chart.command()
    async def all(self, ctx, _round: int = -2):
        data_stream = io.BytesIO()

        async with asqlite.connect("database.sqlite") as conn:
            async with conn.cursor() as cursor:

                await cursor.execute("SELECT * FROM accounts")
                accounts = await cursor.fetchall()

        raw_followers = []

        async with ctx.channel.typing():
            for item in accounts:
                raw_followers.append(round(intersection.user.get_details_for_user(userId=item[1]).followers, _round))

            raw_followers.sort()

            amount_of_followers = list(dict.fromkeys(raw_followers))

            counter = Counter(raw_followers)
            amount_of_users = []

            for item in amount_of_followers:
                amount_of_users.append(counter[item])

            y = amount_of_users # amount of USERS
            x = amount_of_followers # amount of FOLLOWERS

            plt.plot(x,y)

            plt.title("Followers")
            plt.ylabel("Amount of Users")
            plt.xlabel("Amount of Followers")

            plt.savefig(data_stream, format='png', bbox_inches="tight", dpi = 80)
            plt.close()

            data_stream.seek(0)
            chart = discord.File(data_stream,filename="follower_chart.png")

            embed = discord.Embed(timestamp = ctx.message.created_at, color = discord.Color.blue(), title="Follower chart based on raw follower data")
            embed.set_footer(icon_url=ctx.author.avatar_url, text=ctx.author)
            embed.set_image(url="attachment://follower_chart.png")

            await ctx.reply(embed=embed, file=chart, mention_author=False)

    @chart.command()
    async def roles(self, ctx):
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

def setup(client):
    client.add_cog(Chart(client))