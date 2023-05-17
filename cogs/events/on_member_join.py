import discord
from discord.ext import commands

from main import MyClient, logger

class OnMemberJoin(commands.Cog):
    def __init__(self, client: MyClient):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        async with self.client.connection.cursor() as cursor:
            await cursor.execute(f"SELECT * FROM guilds WHERE guild_id = ?", [member.guild.id])
            data = await cursor.fetchone()

        if not data:
            return

        async with self.client.connection.cursor() as cursor:
            await cursor.execute(f"SELECT * FROM accounts WHERE discord_id = {member.id}")
            data = await cursor.fetchone()

        if data:
            await member.add_roles(discord.utils.get(member.guild.roles, name="Verified"))

async def setup(client: commands.Bot):
    await client.add_cog(OnMemberJoin(client))
