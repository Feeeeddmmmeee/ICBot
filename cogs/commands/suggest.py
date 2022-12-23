import discord
from discord.ext import commands
from discord import app_commands

from main import logger

import datetime

class Modal(discord.ui.Modal, title="Suggestion"):
    name = discord.ui.TextInput(label="suggestion title", style=discord.TextStyle.short)
    body = discord.ui.TextInput(label="suggestion", style=discord.TextStyle.paragraph)
    
    def __init__(self, client: commands.Bot, *args, **kwargs):
        self.client = client
        super().__init__(*args, **kwargs)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        if self.client.debug: guild_id = 744653826799435806
        else: guild_id = 469861886960205824

        embed = discord.Embed(
            color=discord.Color.orange(),
            title=self.name,
            description=self.body,
            timestamp=interaction.created_at
        )
        embed.set_footer(text=f"Suggested by {interaction.user}", icon_url=interaction.user.display_avatar.url)

        guild = self.client.get_guild(guild_id)
        channel = discord.utils.get(guild.channels, name="game-suggestions")

        message = await channel.send(embed=embed)

        try:
            await message.add_reaction("<:IC_like:759059895424909380>")
            await message.add_reaction("<:IC_dislike:759060520455766036>")
        except:
            pass
        await message.add_reaction("🤍")
        
        await interaction.followup.send("Suggestion sent.", ephemeral=True)

class Suggest(commands.Cog):

    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @app_commands.command(name="suggest", description="Sends your suggestion to the game suggestions channel.")
    @app_commands.checks.cooldown(1, 60*60, key=lambda interaction: (interaction.guild_id, interaction.user.id))
    async def suggest(self, interaction: discord.Interaction):
        await interaction.response.send_modal(Modal(self.client))

    @suggest.error
    async def on_suggest_error(self, interaction: discord.Interaction, error: app_commands.errors.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            remaining_cooldown = datetime.timedelta(seconds= int(error.retry_after))
            await interaction.response.send_message(f"Please wait {str(remaining_cooldown)[2:-3]} more minutes before running this command again.", ephemeral=True)

async def setup(client: commands.Bot):
    if client.debug:
        await client.add_cog(Suggest(client), guilds=[discord.Object(id=744653826799435806)])
    else:
        await client.add_cog(Suggest(client))