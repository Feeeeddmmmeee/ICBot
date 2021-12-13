import discord, intersection, datetime
from discord.ext import commands
from libs import asqlite

class Getfrom(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True, aliases = ['searchfor'])
    async def getfrom(self, ctx):
        embed = discord.Embed(
                description = f"<:neutral:905485648478228490> This commands requires an argument that can be set to either **name** or **id**!",
                color = discord.Color.blue()
            )

        await ctx.reply(embed=embed, mention_author=False)

    @getfrom.command()
    async def name(self, ctx, *, name):
        account = None
        users = intersection.user.search_for_users(result=10, query=name)

        for user in users:
            if user.name == name:
                account = user

        if not account:
            embed = discord.Embed(
                description = f"<:error:905485648373370890> User not found!",
                color = discord.Color.from_rgb(237, 50, 31)
            )

            await ctx.reply(embed=embed, mention_author=False)
            return

        account = intersection.user.get_details_for_user(userId=account.objectId)

        async with asqlite.connect("database.sqlite") as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS accounts (discord_id INTEGER, ic_id INTEGER)")

                await cursor.execute(f'SELECT discord_id FROM accounts WHERE ic_id = {account.objectId}')
                id = await cursor.fetchone()

        embed = discord.Embed(
            timestamp = ctx.message.created_at,
            color = discord.Color.blue()
        )

        if id:
            user = self.client.get_user(id[0])
            if user:
                embed.set_author(name = user, icon_url = user.avatar_url)
            else: 
                embed.title = f"Searching for `{name}`:"

        embed.add_field(name = "Intersection Controller", value = f"**Nickname:** {account.name}\n**ID:** {account.objectId}\n**Followers:** {account.followers}\n**Last login:** <t:{round(account.lastLogin / 1000.0)}:R>\n**Maps:** {account.maps}")
        embed.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar_url)

        await ctx.reply(embed = embed, mention_author = False)

    @getfrom.command()
    async def id(self, ctx, id):
        account = intersection.user.get_details_for_user(userId=int(id))
        userid = id

        async with asqlite.connect("database.sqlite") as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS accounts (discord_id INTEGER, ic_id INTEGER)")

                await cursor.execute(f'SELECT discord_id FROM accounts WHERE ic_id = {int(id)}')
                id = await cursor.fetchone()

        embed = discord.Embed(
            timestamp = ctx.message.created_at,
            color = discord.Color.blue()
        )

        if id:
            user = self.client.get_user(id[0])
            if user:
                embed.set_author(name = user, icon_url = user.avatar_url)
            else: 
                embed.title = f"Searching for `{userid}`:"

        embed.add_field(name = "Intersection Controller", value = f"**Nickname:** {account.name}\n**ID:** {account.objectId}\n**Followers:** {account.followers}\n**Last login:** <t:{round(account.lastLogin / 1000.0)}:R>\n**Maps:** {account.maps}")
        embed.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar_url)

        await ctx.reply(embed = embed, mention_author = False)


def setup(client):
    client.add_cog(Getfrom(client))