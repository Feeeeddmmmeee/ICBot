import discord, intersection, datetime
from discord.ext import commands
from libs import asqlite

class Map(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command = True)
    async def map(self, ctx, index: int, where = None):
        dislike = self.client.get_emoji(759060520455766036)
        like = self.client.get_emoji(759059895424909380)
        index -= 1;
        discord_id, ic_id = None, None

        if not where: discord_id = ctx.author.id
        elif where.startswith("<"):
            discord_id = int(where.replace("<", "").replace("@", "").replace("!", "").replace(">", ""))
        elif len(where) > 10:
            discord_id = int(where)

        else:
            ic_id = int(where)

        if discord_id:
            async with asqlite.connect("database.sqlite") as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("CREATE TABLE IF NOT EXISTS accounts (discord_id INTEGER, ic_id INTEGER)")

                    await cursor.execute(f'SELECT ic_id FROM accounts WHERE discord_id = {discord_id}')
                    id = await cursor.fetchone()

            if not id:
                embed = discord.Embed(
                description = f"<:error:905485648373370890> This user's account isn't linked!",
                color = discord.Color.from_rgb(237, 50, 31)
                )

                await ctx.reply(embed=embed, mention_author=False)
                return

            account = intersection.user.get_details_for_user(userId = id[0])

            discordid = discord_id

        elif ic_id:
            async with asqlite.connect("database.sqlite") as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("CREATE TABLE IF NOT EXISTS accounts (discord_id INTEGER, ic_id INTEGER)")

                    await cursor.execute(f'SELECT discord_id FROM accounts WHERE ic_id = {ic_id}')
                    account = await cursor.fetchone()

            if account:
                discordid = account[0]

            else:
                discordid = None

            account = intersection.user.get_details_for_user(userId = ic_id)
         
        maps = account.get_user_maps()
        map = maps[index]

        embed = discord.Embed(
            title = f"{map.name} {like} {map.votesUp} {dislike} {map.votesDown} :white_heart: {map.favorites}",
            description = map.desc,
            color = discord.Color.blue(),
            timestamp = ctx.message.created_at
        )
        embed.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar_url)

        if map.gameModeGroup == 1: mode = "Simulation"
        elif map.gameModeGroup == 2: mode = "Traffic Controller"
        elif map.gameModeGroup == 3: mode = "Miscellaneous"

        embed.add_field(name="Game Mode", value=mode)
        embed.add_field(name="Author", value=map.authorName)
        embed.add_field(name="Discord", value=str(self.client.get_user(discordid)))

        embed.add_field(name="Created", value=datetime.datetime.fromtimestamp(round(map.created / 1000.0)))
        embed.add_field(name="Updated", value=datetime.datetime.fromtimestamp(round(map.updated / 1000.0)))
        embed.add_field(name="Version", value=map.mapVersion)

        await ctx.reply(embed = embed, mention_author = False)

    @map.command()
    async def trending(self, ctx, gamemode, time, pos = 1):
        dislike = self.client.get_emoji(759060520455766036)
        like = self.client.get_emoji(759059895424909380)
        pos -= 1

        if gamemode.lower() in ['sim', 'simulation', '1']: gamemode = 1
        elif gamemode.lower() in ['tc', 'trafficcontroller', '2']: gamemode = 2
        #elif gamemode.lower() in ['misc' 'miscellaneous' '3']: gamemode = 3

        map = intersection.map.find_top_maps(gameMode=gamemode, time=time, result=1, page=pos, offset=0)[0]

        async with asqlite.connect("database.sqlite") as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS accounts (discord_id INTEGER, ic_id INTEGER)")

                await cursor.execute(f'SELECT discord_id FROM accounts WHERE ic_id = {map.author}')
                account = await cursor.fetchone()

        if account:
            discordid = account[0]

        else:
            discordid = None

        embed = discord.Embed(
            title = f"{map.name} {like} {map.votesUp} {dislike} {map.votesDown} :white_heart: {map.favorites}",
            description = map.desc,
            color = discord.Color.blue(),
            timestamp = ctx.message.created_at
        )
        embed.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar_url)

        if map.gameModeGroup == 1: mode = "Simulation"
        elif map.gameModeGroup == 2: mode = "Traffic Controller"
        elif map.gameModeGroup == 3: mode = "Miscellaneous"

        embed.add_field(name="Game Mode", value=mode)
        embed.add_field(name="Author", value=map.authorName)
        embed.add_field(name="Discord", value=str(self.client.get_user(discordid)))

        embed.add_field(name="Created", value=datetime.datetime.fromtimestamp(round(map.created / 1000.0)))
        embed.add_field(name="Updated", value=datetime.datetime.fromtimestamp(round(map.updated / 1000.0)))
        embed.add_field(name="Version", value=map.mapVersion)

        await ctx.reply(embed = embed, mention_author = False)

    @map.command()
    async def search(self, ctx, gamemode, *, query):
        if gamemode.lower() in ['sim', 'simulation', '1']: gamemode = 1
        elif gamemode.lower() in ['tc', 'trafficcontroller', '2']: gamemode = 2

        maps = intersection.map.search_for_maps(gameMode=gamemode, result=10, query=query)

        if not len(maps):
            embed = discord.Embed(
                description = f"<:error:905485648373370890> No maps with such a name found!",
                color = discord.Color.from_rgb(237, 50, 31)
            )

            await ctx.reply(embed=embed, mention_author=False)
            return

        embed = discord.Embed(
            title = f"Searching for `{query}`:",
            timestamp = ctx.message.created_at,
            color = discord.Color.blue()
        )

        async with asqlite.connect("database.sqlite") as conn:
            async with conn.cursor() as cursor:
                for map in maps:
                    linked = "Not linked"
                    
                    await cursor.execute(f'SELECT discord_id FROM accounts WHERE ic_id = {map.author}')
                    account = await cursor.fetchone()

                    if account:
                        linked = self.client.get_user(account[0])

                    embed.add_field(name=f"{map.name} <:IC_like:759059895424909380> {map.votesUp} <:IC_dislike:759060520455766036> {map.votesDown} :white_heart: {map.favorites}", value=f"**Author:** {map.authorName} | **Discord:** {linked}", inline=False)

        embed.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar_url)

        await ctx.reply(embed=embed, mention_author=False)

def setup(client):
    client.add_cog(Map(client))