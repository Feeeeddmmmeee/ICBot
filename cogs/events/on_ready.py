import discord
from discord.ext import commands

from main import logger, MyClient, update_roles

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
            await insert_guilds(cursor, 744653826799435806, 469861886960205824)

            await self.client.connection.commit()

            await cursor.execute(f"SELECT * FROM accounts")
            data = await cursor.fetchall()

        activity = discord.Activity(name=f"{len(data)} Linked Accounts", type=discord.ActivityType.watching)
        await self.client.change_presence(status=discord.Status.idle, activity=activity)

        update_roles.start(self.client)
        
async def setup(client: commands.Bot):
    await client.add_cog(OnReady(client))
