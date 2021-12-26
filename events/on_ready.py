import discord
from discord.ext import commands
from libs import asqlite
from main import follower_roles, DEBUG

class On_ready(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        login_info = f">> Logged in as {self.client.user}"
        if DEBUG: login_info += " DEBUG MODE IS ENABLED"

        print(login_info)

        async with asqlite.connect("database.sqlite") as conn:
            async with conn.cursor() as cursor:

                await cursor.execute(f'SELECT * FROM accounts')
                amount_of_users =  await cursor.fetchall()

        activity = discord.Activity(name=f"{len(amount_of_users)} Linked Accounts", type=discord.ActivityType.watching)
        await self.client.change_presence(status=discord.Status.online, activity=activity)

        follower_roles.start()

def setup(client):
    client.add_cog(On_ready(client))