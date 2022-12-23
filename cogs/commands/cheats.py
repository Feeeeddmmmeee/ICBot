import discord
from discord.ext import commands
from discord import app_commands

from main import logger

class Cheats(commands.Cog):

    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @app_commands.command(name="cheats", description="View all the game cheats.")
    async def cheats(self, interaction: discord.Interaction):
        embed = discord.Embed(
                color = discord.Color.orange(),
                description="Here are the current \"cheats\" which will not break the game.\n\n" + "> ` fps        ` Displays an FPS counter.\n> ` regnardet? ` Forces the weather to rain.\n> ` torsvrede  ` Forces the weather to thunderstorm.\n> ` solkatt    ` Forces the weather to sunny.\n> ` dimfilt    ` Forces the weather to fog.\n> ` vaderlek   ` Sets the weather to the default dynamic setting.\n> ` handelser  ` Random events are triggered as often as possible.\n> ` ogonsten   ` Graphics settings not lowered when zooming out.\n> ` gomdasaker ` Unlocks all decorative objects.\n> ` uppdatera  ` Opens the update link for your installation ([shadowtree.se](https://shadowtree-software.se/tr3/lanes3.apk) / [Google Play](https://play.google.com/store/apps/details?id=se.shadowtree.software.trafficbuilder) / [Amazon](https://www.amazon.com/gp/mas/dl/android?p=se.shadowtree.software.trafficbuilder))\n> ` blindstyre ` Disables vehicles stopping before crashed vehicles."
        )
        embed.set_author(name="Intersection Controller Cheats", icon_url=self.client.user.display_avatar.url)
        embed.set_image(url="https://media.discordapp.net/attachments/879324217462632478/1046064114558062683/help.png")
        #embed.add_field(name="<:game:1046100763673382912> Cheats:", value="> ` fps        ` Displays an FPS counter.\n> ` regnardet? ` Forces the weather to rain.\n> ` torsvrede  ` Forces the weather to thunderstorm.\n> ` solkatt    ` Forces the weather to sunny.\n> ` dimfilt    ` Forces the weather to fog.\n> ` vaderlek   ` Sets the weather to the default dynamic setting.\n> ` handelser  ` Random events are triggered as often as possible.\n> ` ogonsten   ` Graphics settings not lowered when zooming out.\n> ` gomdasaker ` Unlocks all decorative objects.\n> ` uppdatera  ` Opens the update link for your installation ([shadowtree.se](https://shadowtree-software.se/tr3/lanes3.apk) / [Google Play](https://play.google.com/store/apps/details?id=se.shadowtree.software.trafficbuilder) / [Amazon](https://www.amazon.com/gp/mas/dl/android?p=se.shadowtree.software.trafficbuilder))\n> ` blindstyre ` Disables vehicles stopping before crashed vehicles.")

        await interaction.response.send_message(embed=embed)

async def setup(client: commands.Bot):
    if client.debug:
        await client.add_cog(Cheats(client), guilds=[discord.Object(id=744653826799435806)])
    else:
        await client.add_cog(Cheats(client))