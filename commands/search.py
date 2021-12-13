import discord, intersection
from discord.ext import commands
from libs import asqlite

class Search(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def search(self, ctx, *, name):
        users = intersection.user.search_for_users(result = 10, query = name)

        if not len(users):
            embed = discord.Embed(
                description = f"<:error:905485648373370890> No users with such a name found!",
                color = discord.Color.from_rgb(237, 50, 31)
            )

            await ctx.reply(embed=embed, mention_author=False)
            return

        embed = discord.Embed(
            title = f"Searching for `{name}`:",
            timestamp = ctx.message.created_at,
            color = discord.Color.blue()
        )

        for user in users:
            linked = "Not linked"
            
            async with asqlite.connect("database.sqlite") as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(f'SELECT discord_id FROM accounts WHERE ic_id = {user.objectId}')
                    account = await cursor.fetchone()

            if account:
                linked = self.client.get_user(account[0])

            embed.add_field(name = user.name, value = f"**ID:** {user.objectId} | **Discord:** {linked}", inline = False)

        embed.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar_url)


        await ctx.reply(embed=embed, mention_author = False)

def setup(client):
    client.add_cog(Search(client))
  