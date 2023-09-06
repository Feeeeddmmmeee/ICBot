import discord
from discord.ext import commands
from discord import app_commands

from main import logger

class Unlink(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="unlink", description="Unlinks an account from the selected user.")
    @app_commands.describe(user = "Who to unlink an account from.")
    @app_commands.default_permissions(manage_guild=True)
    async def unlink(self, interaction: discord.Interaction, user: discord.Member):
        async with self.client.connection.cursor() as cursor:
            await cursor.execute(f"SELECT * FROM guilds WHERE guild_id = ?", [interaction.guild_id])
            data = await cursor.fetchone()

        if not data:
            await interaction.response.send_message("This command cannot be ran in this server.", ephemeral=True)
            return
        
        async with self.client.connection.cursor() as cursor:
            await cursor.execute("SELECT ic_id FROM accounts WHERE discord_id = ?", [user.id])
            data = await cursor.fetchone()

            if not data:
                await interaction.response.send_message(f"{user}'s account is not linked!", ephemeral= True)
                return

            await cursor.execute("DELETE FROM accounts WHERE discord_id = ?", [user.id])
            await self.client.connection.commit()

            logger.debug(f"Unlinked account for user {user}")

            await cursor.execute(f"SELECT * FROM accounts")
            data = await cursor.fetchall()

        await user.remove_roles(discord.utils.get(interaction.guild.roles, name="Verified"))

        activity = discord.Activity(name=f"{len(data)} Linked Accounts", type=discord.ActivityType.watching)
        await self.client.change_presence(status=discord.Status.idle, activity=activity)

        await interaction.response.send_message("Account successfully unlinked.", ephemeral=True)
        
async def setup(client: commands.Bot):
    if client.debug:
        await client.add_cog(Unlink(client), guilds=[discord.Object(id=744653826799435806)])
    else:
        await client.add_cog(Unlink(client))
