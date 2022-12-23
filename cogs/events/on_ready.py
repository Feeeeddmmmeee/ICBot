import discord
from discord.ext import commands

from main import logger, MyClient

import aiosqlite

async def insert_guilds(cursor: aiosqlite.Cursor, *args):
    for guild in args:
        await cursor.execute(f"SELECT * FROM guilds WHERE guild_id = ?", [guild])
        if not await cursor.fetchone():
            await cursor.execute("INSERT INTO guilds(guild_id) VALUES(?)", [guild])

class OnReady(commands.Cog):
    def __init__(self, client: MyClient):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"Logged in as {self.client.user}")

        async with self.client.connection.cursor() as cursor:
            await cursor.execute("DROP TABLE IF EXISTS color_tags")
            await cursor.execute("DROP TABLE IF EXISTS colors")
            await cursor.execute("DROP TABLE IF EXISTS tags")
            await cursor.execute("DROP TABLE IF EXISTS color_votes")

            await cursor.execute("""CREATE TABLE IF NOT EXISTS accounts (
                discord_id INTEGER, 
                ic_id INTEGER, 
                linked_at INTEGER)""")

            await cursor.execute("CREATE TABLE IF NOT EXISTS guilds (guild_id INTEGER)")
            await cursor.execute("""CREATE TABLE IF NOT EXISTS colors (
                user_id INTEGER, 
                submission_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                color INTEGER, 
                upvotes INTEGER DEFAULT 1, 
                downvotes INTEGER DEFAULT 0, 
                created INTEGER)""")
            
            await cursor.execute("""CREATE TABLE IF NOT EXISTS tags (
                tag_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                tag_name TEXT)""")

            await cursor.execute("""CREATE TABLE IF NOT EXISTS color_tags (
                submission_id INTEGER, 
                tag_id INTEGER)""")

            await cursor.execute("""CREATE TABLE IF NOT EXISTS color_votes (
                user_id INTEGER, 
                submission_id INTEGER, 
                vote INTEGER)""")

            await insert_guilds(cursor, 744653826799435806, 469861886960205824)

            await self.client.connection.commit()

            await cursor.execute(f"SELECT * FROM accounts")
            data = await cursor.fetchall()

        activity = discord.Activity(name=f"{len(data)} Linked Accounts", type=discord.ActivityType.watching)
        await self.client.change_presence(status=discord.Status.idle, activity=activity)

async def setup(client: commands.Bot):
    await client.add_cog(OnReady(client))