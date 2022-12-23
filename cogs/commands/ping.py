import discord
from discord.ext import commands
from discord import app_commands

from main import logger

class Ping(commands.Cog):

    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @app_commands.command(name="ping", description="Check the bot's ping.")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Pong! Took {round(self.client.latency * 1000)}ms.", ephemeral=True)

async def setup(client: commands.Bot):
    if client.debug:
        await client.add_cog(Ping(client), guilds=[discord.Object(id=744653826799435806)])
    else:
        await client.add_cog(Ping(client))