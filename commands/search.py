import discord, intersection, sqlite3
from discord.ext import commands

class Search(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def search(self, ctx, *, name):
        database = sqlite3.connect("database.sqlite")
        cursor = database.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS accounts (discord_id INTEGER, ic_id INTEGER)")

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
            
            cursor.execute(f'SELECT discord_id FROM accounts WHERE ic_id = {user.objectId}')
            account = cursor.fetchone()

            if account:
                linked = self.client.get_user(account[0])

            embed.add_field(name = user.name, value = f"**ID:** {user.objectId} | **Discord:** {linked}", inline = False)

        embed.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar_url)

        cursor.close()
        database.close()

        await ctx.reply(embed=embed, mention_author = False)

def setup(client):
    client.add_cog(Search(client))
  