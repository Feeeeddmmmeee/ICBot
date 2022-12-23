import discord
from discord.ext import commands
from discord import app_commands

from main import logger, MyClient
from typing import List, Union
import datetime
import tl3api

class Navigation(discord.ui.View):
    def __init__(self, client: MyClient, list: Union[List[tl3api.Map], List[tl3api.User]], index = 0, *, timeout = 120):
        self.client = client
        self.index = index
        self.list = list
        super().__init__(timeout=timeout)

    async def update_embed(self, interaction: discord.Interaction):
        pass

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
        if self.index > 99: self.index = 99
        await self.update_embed(interaction)

    @discord.ui.button(emoji="<:first:1046447978824613918>", style=discord.ButtonStyle.grey)
    async def last(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index = 99
        await self.update_embed(interaction)

class MapNavigation(Navigation):
    async def update_embed(self, interaction: discord.Interaction):
        await interaction.response.defer()

        if self.index >= len(self.list): self.index = len(self.list) - 1
        map = self.list[self.index]

        async with self.client.connection.cursor() as cursor:
            await cursor.execute(f"SELECT discord_id FROM accounts WHERE ic_id = {map.author}")
            discord_id = await cursor.fetchone()

        user = None
        if discord_id:
            user = await self.client.fetch_user(discord_id[0])

        if not user: user = "Not linked"

        embed = discord.Embed(
            timestamp=datetime.datetime.now(),
            color=discord.Color.orange(),
            title=map,
            description=map.desc
        )

        mode = ["Simulation", "Traffic Controller", "Miscellaneous"][map.game_mode_group - 1]
        embed.add_field(name="Map", value=f"> ` Game mode ` {mode}\n> ` Version   ` {map.map_version}\n> ` Created   ` <t:{round(map.created / 1000.0)}:R>\n> ` Updated   ` <t:{round(map.updated / 1000.0)}:R>")
        embed.add_field(name="User", value=f"> ` Nickname   ` {map.author_name}\n> ` ID         ` {map.author}\n> ` Last login ` <t:{round((await map.get_author()).last_login / 1000.0)}:R>\n> ` Discord    ` {user}")
        embed.set_image(url="https://media.discordapp.net/attachments/879324217462632478/1046064114558062683/help.png")
        embed.set_footer(text = f"Page {self.index + 1}/{len(self.list)}, 👍{map.votes_up} 👎{map.votes_down} ❤️{map.favorites}")

        await interaction.followup.edit_message(interaction.message.id, embed=embed, view=MapNavigation(self.client, self.list, self.index))

class UserNavigation(Navigation):
    async def update_embed(self, interaction: discord.Interaction):
        await interaction.response.defer()

        if self.index >= len(self.list): self.index = len(self.list) - 1
        user = self.list[self.index]

        async with self.client.connection.cursor() as cursor:
            await cursor.execute(f"SELECT discord_id, linked_at FROM accounts WHERE ic_id = ?", [user.object_id])
            data = await cursor.fetchone()

        embed = discord.Embed(
            timestamp=datetime.datetime.now(),
            color=discord.Color.orange(),
            description=f"> ` Nickname   ` {user}\n > ` ID         ` {user.object_id}\n> ` Followers  ` {user.followers}\n> ` Last login ` <t:{round(user.last_login / 1000.0)}:R>"
        )
        embed.set_footer(text = f"Page {self.index + 1}/{len(self.list)}")

        if data:
            discord_user = await self.client.fetch_user(data[0])
            embed.set_author(name = discord_user, icon_url=discord_user.display_avatar.url)
            embed.description += f"\n> ` Linked     ` <t:{round(data[1] / 1000.0)}:R>\n> ` Maps       ` {user.maps}"

        else:
            embed.set_author(name=user)
            embed.description += f"\n> ` Linked     ` Not linked\n> ` Maps       ` {user.maps}"

        await interaction.followup.edit_message(interaction.message.id, embed=embed, view=UserNavigation(self.client, self.list, self.index))

class Search(commands.GroupCog, group_name="search"):

    def __init__(self, client: MyClient) -> None:
        self.client = client
        super().__init__()

    @app_commands.command(name="users", description="Search for IC users.")
    @app_commands.describe(query="Name to search for.")
    @app_commands.describe(offset="Which index to start the search at (defaults to 0).")
    @app_commands.describe(page="Page to start the search at (defaults to 0 i.e. the first one).")
    async def users(self, interaction: discord.Interaction, query: str, offset: int = 0, page: int = 0):
        await interaction.response.defer()
        users = await self.client.ic.search_for_users(query=query, result=100, page=page)
        if not len(users):
            await interaction.followup.send("No users with such a name found.", ephemeral=True)
            return

        user = users[offset]

        async with self.client.connection.cursor() as cursor:
            await cursor.execute(f"SELECT discord_id, linked_at FROM accounts WHERE ic_id = ?", [user.object_id])
            data = await cursor.fetchone()

        embed = discord.Embed(
            timestamp=datetime.datetime.now(),
            color=discord.Color.orange(),
            description=f"> ` Nickname   ` {user}\n > ` ID         ` {user.object_id}\n> ` Followers  ` {user.followers}\n> ` Last login ` <t:{round(user.last_login / 1000.0)}:R>"
        )
        embed.set_footer(text = f"Page {offset + 1}/{len(users)}")

        if data:
            discord_user = await self.client.fetch_user(data[0])
            logger.info(discord_user)
            embed.set_author(name = discord_user, icon_url=discord_user.display_avatar.url)
            embed.description += f"\n> ` Linked     ` <t:{round(data[1] / 1000.0)}:R>\n> ` Maps       ` {user.maps}"

        else:
            embed.set_author(name=user)
            embed.description += f"\n> ` Linked     ` Not linked\n> ` Maps       ` {user.maps}"

        await interaction.followup.send(embed=embed, view=UserNavigation(self.client, users, offset))

    @app_commands.command(name="maps", description="Search for IC maps.")
    @app_commands.choices(mode = [
        app_commands.Choice(name="Simulation", value="1"),
        app_commands.Choice(name="Traffic Controller", value="2"),
        app_commands.Choice(name="Miscellaneous", value="3")
    ])
    @app_commands.describe(mode = "Game mode.", query="Name to search for.")
    @app_commands.describe(offset="Which index to start the search at (defaults to 0).")
    @app_commands.describe(page="Page to start the search at (defaults to 0 i.e. the first one).")
    async def maps(self, interaction: discord.Interaction, mode: str, query: str, offset: int = 0, page: int = 0):
        await interaction.response.defer()
        mode = int(mode)
        maps = await self.client.ic.search_for_maps(game_mode=mode, result=100, query=query, page=page)
        if not len(maps):
            await interaction.followup.send("No maps with such a name found.", ephemeral=True)
            return

        map = maps[offset]

        async with self.client.connection.cursor() as cursor:
            await cursor.execute(f"SELECT discord_id FROM accounts WHERE ic_id = ?", [map.author])
            discord_id = await cursor.fetchone()

        user = "Not linked"
        if discord_id:
            user = await self.client.fetch_user(discord_id[0])

        embed = discord.Embed(
            timestamp=datetime.datetime.now(),
            color=discord.Color.orange(),
            title=map,
            description=map.desc
        )

        temp_mode = mode
        mode = ["Simulation", "Traffic Controller", "Miscellaneous"][mode - 1]
        embed.add_field(name="Map", value=f"> ` Game mode ` {mode}\n> ` Version   ` {map.map_version}\n> ` Created   ` <t:{round(map.created / 1000.0)}:R>\n> ` Updated   ` <t:{round(map.updated / 1000.0)}:R>")
        embed.add_field(name="User", value=f"> ` Nickname   ` {map.author_name}\n> ` ID         ` {map.author}\n> ` Last login ` <t:{round((await map.get_author()).last_login / 1000.0)}:R>\n> ` Discord    ` {user}")
        embed.set_image(url="https://media.discordapp.net/attachments/879324217462632478/1046064114558062683/help.png")
        embed.set_footer(text = f"Page 1/{len(maps)}, 👍{map.votes_up} 👎{map.votes_down} ❤️{map.favorites}")

        await interaction.followup.send(embed=embed, view=MapNavigation(self.client, maps, offset))

    @app_commands.command(name="colors", description="Search for colors in the hex color database.")
    @app_commands.choices(order = [
        app_commands.Choice(name="Top", value="1"),
        app_commands.Choice(name="New", value="2")
    ])
    @app_commands.describe(order="In what order to return the search results.", tags="Tags to search for (separated by spaces)")
    async def colors(self, interaction: discord.Interaction, order: str, tags: str = None):
        await interaction.response.defer()
        
        if order == "1":
            pass
        else:
            pass

async def setup(client: commands.Bot):
    if client.debug:
        await client.add_cog(Search(client), guilds=[discord.Object(id=744653826799435806)])
    else:
        await client.add_cog(Search(client))