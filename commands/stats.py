import discord, intersection, datetime
from discord.ext import commands
from numpy import average
from libs import asqlite

class Stats(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def stats(self, ctx, *, where: str = None):
        discord_id = 0
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
                    ic_id = await cursor.fetchone()

            if not ic_id:
                embed = discord.Embed(
                    description = f"<:error:905485648373370890> This user's account isn't linked!",
                    color = discord.Color.from_rgb(237, 50, 31)
                )

                await ctx.reply(embed=embed, mention_author=False)
                return

        ic_id = ic_id[0]

        account = intersection.user.get_details_for_user(userId = ic_id)
        maps = account.get_user_maps()

        total = [0, 0, 0, 0]
        top = [0, 0, 0]
        average = [0, 0, 0]
        dislike = self.client.get_emoji(759060520455766036)
        like = self.client.get_emoji(759059895424909380)

        popular = maps[0]
        ratio = maps[0]

        for map in maps:
            if map.votesUp > top[0]: top[0] = map.votesUp
            if map.votesDown > top[1]: top[1] = map.votesDown
            if map.favorites > top[2]: top[2] = map.favorites

            total[0] += map.votesUp
            total[1] += map.votesDown
            total[2] += map.favorites
            total[3] += map.mapVersion

            average[0] += map.votesUp
            average[1] += map.votesDown
            average[2] += map.favorites

            if map.votesUp - map.votesDown > popular.votesUp - popular.votesDown: popular = map
            if (map.votesUp - map.votesDown) / map.mapVersion > (ratio.votesUp - ratio.votesDown) / ratio.mapVersion: ratio = map

        for i in range(3): average[i] /= account.maps
        for i in range(3): average[i] = round(average[i], 1)

        embed = discord.Embed(
            timestamp = ctx.message.created_at,
            color = discord.Color.blue(),
            description = f"**Most Popular Map:**\n{popular.name} - {like} {popular.votesUp} {dislike} {popular.votesDown} 🤍 {popular.favorites}\nScore: {popular.votesUp - popular.votesDown}, Ratio: {round((popular.votesUp - popular.votesDown)/popular.mapVersion, 1)}" + "\n\n" + f"**Highest (likes - dislikes)/updates Ratio:**\n{ratio.name} - {like} {ratio.votesUp} {dislike} {ratio.votesDown} 🤍 {ratio.favorites}\nScore: {ratio.votesUp - ratio.votesDown}, Ratio: {round((ratio.votesUp - ratio.votesDown)/ratio.mapVersion, 1)}\n\nAverage Ratio: {round((total[0] - total[1])/total[3], 1)}"
        )

        if discord_id:
            user = self.client.get_user(discord_id)
            embed.set_author(name = f"{user} - {account.name}", icon_url = user.avatar_url)
        else:
            async with asqlite.connect("database.sqlite") as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("CREATE TABLE IF NOT EXISTS accounts (discord_id INTEGER, ic_id INTEGER)")

                    await cursor.execute(f'SELECT discord_id FROM accounts WHERE ic_id = {ic_id}')
                    discord_id = (await cursor.fetchone())[0]
            
            if discord_id:
                user = self.client.get_user(discord_id)
                embed.set_author(name = f"{user} - {account.name}", icon_url = user.avatar_url)

            else: embed.set_author(name = f"{account.name}")

        embed.add_field(name="Total Stats", value=f"{like} {total[0]}\n{dislike} {total[1]}\n🤍 {total[2]}")
        embed.add_field(name="Top Stats", value=f"{like} {top[0]}\n{dislike} {top[1]}\n🤍 {top[2]}")
        embed.add_field(name="Average Stats", value=f"{like} {average[0]}\n{dislike} {average[1]}\n🤍 {average[2]}")

        await ctx.reply(embed = embed, mention_author = False)

def setup(client):
    client.add_cog(Stats(client))