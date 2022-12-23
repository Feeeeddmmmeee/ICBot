import discord
from discord.ext import commands
from discord import app_commands

from main import logger, MyClient

import tl3api
import time

class Link(commands.Cog):
    def __init__(self, client: MyClient):
        self.client = client

    @app_commands.command(name="link", description="Links an account to the selected user.")
    @app_commands.describe(user = "User to link an account to.", id = "The user's IC account ID.")
    @app_commands.default_permissions(manage_guild=True)
    async def link(self, interaction: discord.Interaction, user: discord.Member, id: int):
        async with self.client.connection.cursor() as cursor:
            await cursor.execute(f"SELECT * FROM guilds WHERE guild_id = ?", [interaction.guild_id])
            data = await cursor.fetchone()

        if not data:
            await interaction.response.send_message("This command cannot be ran in this server.", ephemeral=True)
            return

        try:
            ic = await self.client.ic.get_details_for_user(user_id=id)
        except:
            await interaction.response.send_message("No user with such an id exists in the game.", ephemeral=True)
            return
        
        async with self.client.connection.cursor() as cursor:
            await cursor.execute("SELECT ic_id FROM accounts WHERE discord_id = ?", [user.id])
            data = await cursor.fetchone()

            timestamp = round(time.time() * 1000)

            if data:
                await cursor.execute("UPDATE accounts SET ic_id = ?, linked_at = ? WHERE discord_id = ?", [ic.object_id, timestamp, user.id])
                logger.debug(f"Account for user {user} updated")
            else:
                await cursor.execute("INSERT INTO accounts(discord_id, ic_id, linked_at) VALUES(?, ?, ?)", [user.id, ic.object_id, timestamp])
                logger.debug(f"Linked account for user {user}")
            
            await self.client.connection.commit()

            await cursor.execute(f"SELECT * FROM accounts")
            data = await cursor.fetchall()

        activity = discord.Activity(name=f"{len(data)} Linked Accounts", type=discord.ActivityType.watching)
        await self.client.change_presence(status=discord.Status.idle, activity=activity)

        await interaction.response.send_message("Account successfully linked.", ephemeral=True)

async def setup(client: commands.Bot):
    if client.debug:
        await client.add_cog(Link(client), guilds=[discord.Object(id=744653826799435806)])
    else:
        await client.add_cog(Link(client))
