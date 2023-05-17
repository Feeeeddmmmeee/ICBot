import discord
from discord.ext import commands
from discord import app_commands

HELP_EMBED = discord.Embed(
    color = discord.Color.orange(),
    description="Use the selection menu below to navigate to your desired submenu. Each submenu contains detailed information about its subject.\n\n<:menu_emoji:1046072165285507092> **Submenus:**\n\n> <:slash_emoji:1046070144738275348> **Commands** - View the list of all the commands.\n> \n > <:link_emoji:1046070628698030210> **Links** - Helpful links.\n> \n > <:folder_emoji:1046075556149596321> **Other** - Everything else. "
)

class Buttons(discord.ui.View):
    def __init__(self, client: commands.Bot, *, timeout = 120):
        self.client = client
        super().__init__(timeout=timeout)

    @discord.ui.button(label="Go Back", emoji="<:arrow:1046081153737687080>", style=discord.ButtonStyle.grey)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        HELP_EMBED.set_author(name="Intersection Controller Help", icon_url=self.client.user.display_avatar.url)
        HELP_EMBED.set_image(url="https://media.discordapp.net/attachments/879324217462632478/1046064114558062683/help.png")
        await interaction.response.edit_message(embed=HELP_EMBED, view=SelectView(self.client))

class Select(discord.ui.Select):
    def __init__(self, client: commands.Bot):
        self.client = client
        options = [
            discord.SelectOption(label="Commands", emoji="<:slash_emoji:1046070144738275348>", description="View the list of all the commands."),
            discord.SelectOption(label="Links", emoji="<:link_emoji:1046070628698030210>", description="Helpful links."),
            discord.SelectOption(label="Other", emoji="<:folder_emoji:1046075556149596321>", description="Everything else.")
        ]
        super().__init__(placeholder="Choose an option", max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "Commands":
            embed = discord.Embed(
                color = discord.Color.orange(),
                description="Below are all the currently available commands."
            )
            embed.set_author(name="Intersection Controller Commands", icon_url=self.client.user.display_avatar.url)
            embed.set_image(url="https://media.discordapp.net/attachments/879324217462632478/1046064114558062683/help.png")
            embed.add_field(name="<:game:1046100763673382912> IC & Discord:", value="> ` profile ` Displays information about a user's IC account.\n> ` cheats  ` Sends a list of all the available game cheats.\n> ` verify  ` Starts the verification process.\n> ` search  ` ` [users/maps/colors] ` Searches the specified database.\n> ` submit  ` Adds the specified color to the database.", inline=False)
            embed.add_field(name="<:staff:1046098417367142460> Admin:",value="> ` link   ` Links an account to the user.\n> ` unlink ` Removes the linked account from the user.\n> ` debug  ` Executes code. Owner only.",inline=False)
            embed.add_field(name="<:folder_emoji:1046075556149596321> Miscellaneous:", value="> ` help ` Sends this embed.\n> ` ping ` Check's the bot's latency.",inline=False)

            await interaction.response.edit_message(embed=embed, view=Buttons(self.client))
        elif self.values[0] == "Links":
            embed = discord.Embed(
                color = discord.Color.orange(),
                description="Links which you might find useful."
            )
            embed.set_author(name="Intersection Controller Links", icon_url=self.client.user.display_avatar.url)
            embed.set_image(url="https://media.discordapp.net/attachments/879324217462632478/1046064114558062683/help.png")
            embed.add_field(name="<:link_emoji:1046070628698030210> Links:", value="> [` Discord Invite `](https://discord.gg/bxUC8sw64U) Invite other people to the server.\n> [` Game's Website `](https://shadowtree-software.se/trafficlanes3.html) Information about the game.\n> [` Google Play    `](https://play.google.com/store/apps/details?id=se.shadowtree.software.trafficbuilder&hl=en&gl=US) You can download the game here.\n> [` Github         `](https://github.com/Feeeeddmmmeee/ICBot) This bot's source code.")

            await interaction.response.edit_message(embed=embed, view=Buttons(self.client))
        elif self.values[0] == "Other":
            pass

class SelectView(discord.ui.View):
    def __init__(self, client: commands.Bot, *, timeout = 120):
        super().__init__(timeout=timeout)
        self.add_item(Select(client))

class Help(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @app_commands.command(name="help", description="View the help menu.")
    async def help(self, interaction: discord.Interaction):
        HELP_EMBED.set_author(name="Intersection Controller Help", icon_url=self.client.user.display_avatar.url)
        HELP_EMBED.set_image(url="https://media.discordapp.net/attachments/879324217462632478/1046064114558062683/help.png")

        await interaction.response.send_message(embed=HELP_EMBED, view=SelectView(self.client))

async def setup(client: commands.Bot):
    if client.debug:
        await client.add_cog(Help(client), guilds=[discord.Object(id=744653826799435806)])
    else:
        await client.add_cog(Help(client))
