import discord, intersection, datetime
from discord.ext import commands
from libs import asqlite

class Profile(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ['userinfo', 'discord', 'user', 'ui', 'whois'])
    async def profile(self, ctx, user: discord.User = None):
        if not user: user = ctx.author
        await ctx.trigger_typing()

        async with asqlite.connect("database.sqlite") as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS accounts (discord_id INTEGER, ic_id INTEGER)")

                await cursor.execute(f'SELECT ic_id FROM accounts WHERE discord_id = {user.id}')
                id = await cursor.fetchone()

        if not id:
            embed = discord.Embed(
                description = f"<:error:905485648373370890> This user's account isn't linked!",
                color = discord.Color.from_rgb(237, 50, 31)
            )

            await ctx.reply(embed=embed, mention_author=False)
            return

        account = intersection.user.get_details_for_user(userId = id[0])

        embed = discord.Embed(
            timestamp = ctx.message.created_at,
            color = discord.Color.blue()
        )

        embed.set_author(name = user, icon_url = user.avatar_url)
        embed.add_field(name = "Intersection Controller", value = f"**Nickname:** {account.name}\n**ID:** {account.objectId}\n**Followers:** {account.followers}\n**Last login:** {datetime.datetime.fromtimestamp(round(account.lastLogin / 1000.0))}\n**Maps:** {account.maps}")
        embed.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar_url)

        await ctx.reply(embed = embed, mention_author = False)

def setup(client):
    client.add_cog(Profile(client))