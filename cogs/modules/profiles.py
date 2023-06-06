import discord
from discord.ext import commands
from discord import app_commands

from main import logger, MyClient

import tl3api
import datetime

class Navigation(discord.ui.View):
    def __init__(self, client: MyClient, user: discord.Member, index = 0, *, timeout = 120):
        self.client = client
        self.index = index
        self.user = user
        super().__init__(timeout=timeout)

    async def update_embed(self, interaction: discord.Interaction):
        async with self.client.connection.cursor() as cursor:
            await cursor.execute(f"SELECT ic_id FROM accounts WHERE discord_id = {self.user.id}")
            ic_id = await cursor.fetchone()

        if not ic_id:
            await interaction.response.send_message("This user's account is not linked.", ephemeral=True)
            return

        ic_account = await self.client.ic.get_details_for_user(user_id=ic_id[0])

        if not ic_account.maps:
            await interaction.response.send_message("This user hasn't uploaded any maps.", ephemeral=True)
            return

        if self.index >= ic_account.maps: self.index = ic_account.maps - 1
        elif self.index < 0: self.index = 0

        map = (await ic_account.get_user_maps())[self.index]

        mode = "Miscellaneous"
        if map.game_mode_group == 1: mode = "Simulation"
        elif map.game_mode_group == 2: mode = "Traffic Controller"

        embed = discord.Embed(
            timestamp=datetime.datetime.now(),
            color=discord.Color.orange(),
            title=map,
            description=map.desc
        )
        embed.add_field(name="Map", value=f"> ` Game mode ` {mode}\n> ` Version   ` {map.map_version}\n> ` Created   ` <t:{round(map.created / 1000.0)}:R>\n> ` Updated   ` <t:{round(map.updated / 1000.0)}:R>")
        embed.add_field(name="User", value=f"> ` Nickname   ` {map.author_name}\n> ` ID         ` {map.author}\n> ` Last login ` <t:{round(ic_account.last_login / 1000.0)}:R>\n> ` Discord    ` {self.user}")
        embed.set_image(url="https://media.discordapp.net/attachments/879324217462632478/1046064114558062683/help.png")
        embed.set_footer(text = f"Page {self.index + 1}/{ic_account.maps}, 👍{map.votes_up} 👎{map.votes_down} ❤️{map.favorites}")

        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(emoji="<:last:1046448014564266146>", style=discord.ButtonStyle.grey)
    async def first(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index = 0
        await self.update_embed(interaction)

    @discord.ui.button(emoji="<:arrow:1046081153737687080>", style=discord.ButtonStyle.grey)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index -= 1
        if self.index < 0: self.index = 0
        await self.update_embed(interaction)

    @discord.ui.button(emoji="<:arrowR:1046384022726656040>", style=discord.ButtonStyle.grey)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index += 1
        await self.update_embed(interaction)

    @discord.ui.button(emoji="<:first:1046447978824613918>", style=discord.ButtonStyle.grey)
    async def last(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index = 50
        await self.update_embed(interaction)

class ViewMaps(discord.ui.View):
    def __init__(self, instance: commands.Cog, client: commands.Bot, user: discord.Member, *, timeout = 120):
        self.instance = instance
        self.client = client
        self.user = user
        super().__init__(timeout=timeout)

    @discord.ui.button(label="View Maps", style=discord.ButtonStyle.grey)
    async def on_click(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.instance.create_map_info_embed(interaction, self.user)

class Profile(commands.Cog):

    def __init__(self, client: MyClient) -> None:
        self.client = client
        self.profile_context_menu_message = app_commands.ContextMenu(
            name="See profile",
            callback=self.profile_context_menu_message_callback
        )
        self.map_context_menu_message = app_commands.ContextMenu(
            name="See maps",
            callback = self.map_context_menu_message_callback
        )
        self.profile_context_menu_user = app_commands.ContextMenu(
            name="See profile",
            callback=self.create_profile_info_embed
        )
        self.map_context_menu_user = app_commands.ContextMenu(
            name="See maps",
            callback = self.create_map_info_embed
        )
        if client.debug:
            self.client.tree.add_command(self.profile_context_menu_message, guilds=[discord.Object(id=744653826799435806)])
            self.client.tree.add_command(self.map_context_menu_message, guilds=[discord.Object(id=744653826799435806)])
            self.client.tree.add_command(self.profile_context_menu_user, guilds=[discord.Object(id=744653826799435806)])
            self.client.tree.add_command(self.map_context_menu_user, guilds=[discord.Object(id=744653826799435806)])
        else:
            self.client.tree.add_command(self.profile_context_menu_message)
            self.client.tree.add_command(self.map_context_menu_message)
            self.client.tree.add_command(self.profile_context_menu_user)
            self.client.tree.add_command(self.map_context_menu_user)

    @app_commands.command(name="profile", description="View a user's profile.")
    @app_commands.describe(user = "User whose profile you want to see.")
    async def profile(self, interaction: discord.Interaction, user: discord.User = None):
        if not user: user = interaction.user
        await self.create_profile_info_embed(interaction, user)

    async def profile_context_menu_message_callback(self, interaction: discord.Interaction, message: discord.Message):
        await self.create_profile_info_embed(interaction, message.author)

    async def map_context_menu_message_callback(self, interaction: discord.Interaction, messasge: discord.Message):
        await self.create_map_info_embed(interaction, messasge.author)

    async def create_profile_info_embed(self, interaction: discord.Interaction, user: discord.Member) -> None:
        if isinstance(user, discord.Message): user = user.author
        async with self.client.connection.cursor() as cursor:
            await cursor.execute(f"SELECT ic_id, linked_at FROM accounts WHERE discord_id = {user.id}")
            data = await cursor.fetchone()

        if not data:
            await interaction.response.send_message("This user's account is not linked.", ephemeral=True)
            return

        logger.debug("Fetching Intersection Controller data")
        ic_account = await self.client.ic.get_details_for_user(user_id=data[0])

        embed = discord.Embed(
            color=discord.Color.orange(),
            description=f"> ` Nickname   ` {ic_account}\n > ` ID         ` {ic_account.object_id}\n> ` Followers  ` {ic_account.followers}\n> ` Last login ` <t:{round(ic_account.last_login / 1000.0)}:R>\n> ` Linked     ` <t:{round(data[1] / 1000.0)}:R>\n> ` Maps       ` {ic_account.maps}"
        )

        embed.set_author(name = user, icon_url=user.display_avatar.url)

        await interaction.response.send_message(embed=embed, view=ViewMaps(self, self.client, user))

    async def create_map_info_embed(self, interaction: discord.Interaction, user: discord.Member) -> None:
        if isinstance(user, discord.Message): user = user.author
        async with self.client.connection.cursor() as cursor:
            await cursor.execute(f"SELECT ic_id FROM accounts WHERE discord_id = {user.id}")
            ic_id = await cursor.fetchone()

        if not ic_id:
            await interaction.response.send_message("This user's account is not linked.", ephemeral=True)
            return

        ic_account = await self.client.ic.get_details_for_user(user_id=ic_id[0])

        if not ic_account.maps:
            await interaction.response.send_message("This user hasn't uploaded any maps.", ephemeral=True)
            return

        index = 0
        map = (await ic_account.get_user_maps())[index]

        mode = ["Simulation", "Traffic Controller", "Miscellaneous"][map.game_mode_group - 1]

        embed = discord.Embed(
            timestamp=datetime.datetime.now(),
            color=discord.Color.orange(),
            title=map,
            description=map.desc
        )
        embed.add_field(name="Map", value=f"> ` Game mode ` {mode}\n> ` Version   ` {map.map_version}\n> ` Created   ` <t:{round(map.created / 1000.0)}:R>\n> ` Updated   ` <t:{round(map.updated / 1000.0)}:R>")
        embed.add_field(name="User", value=f"> ` Nickname   ` {map.author_name}\n> ` ID         ` {map.author}\n> ` Last login ` <t:{round(ic_account.last_login / 1000.0)}:R>\n> ` Discord    ` {user}")
        embed.set_image(url="https://media.discordapp.net/attachments/879324217462632478/1046064114558062683/help.png")
        embed.set_footer(text = f"Page {index + 1}/{ic_account.maps}, 👍{map.votes_up} 👎{map.votes_down} ❤️{map.favorites}")

        if interaction.message:
            await interaction.response.edit_message(embed=embed, view=Navigation(self.client, user))
        else:
            await interaction.response.send_message(embed=embed, view=Navigation(self.client, user))

async def setup(client: commands.Bot):
    if client.debug:
        await client.add_cog(Profile(client), guilds=[discord.Object(id=744653826799435806)])
    else:
        await client.add_cog(Profile(client))
