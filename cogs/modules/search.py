from io import BytesIO
import discord
from discord.ext import commands
from discord import app_commands

from main import logger, MyClient
import datetime
from PIL import Image

class Navigation(discord.ui.View):
    def __init__(self, client: MyClient, list, index = 0, *, timeout = 120):
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
        if self.index >= len(self.list): self.index = len(self.list) - 1
        await self.update_embed(interaction)

    @discord.ui.button(emoji="<:first:1046447978824613918>", style=discord.ButtonStyle.grey)
    async def last(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index = len(self.list) - 1
        await self.update_embed(interaction)

class ColorNavigation(Navigation):

    @discord.ui.button(emoji="👍", style=discord.ButtonStyle.grey, row=1)
    async def upvote(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.vote(interaction, 1)

    @discord.ui.button(emoji="👎", style=discord.ButtonStyle.grey, row=1)
    async def downvote(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.vote(interaction, -1)

    async def vote(self, interaction: discord.Interaction, vote: int):
        vote_type = "upvotes" if vote > 0 else "downvotes"
        async with self.client.connection.cursor() as cursor:
            await cursor.execute("""
                SELECT
                    vote
                FROM
                    color_votes
                WHERE
                    submission_id = ?
                AND
                    user_id = ?
            """, [self.list[self.index][1], interaction.user.id])
            data = await cursor.fetchone()

            if data:
                await cursor.execute("""
                    UPDATE
                        color_votes
                    SET
                        vote = ?
                    WHERE
                        submission_id = ?
                    AND 
                        user_id = ?
                """, [vote, self.list[self.index][1], interaction.user.id])

                if data[0] != vote:
                    previous_vote = ["upvotes", "downvotes"][1 if vote > 0 else 0]
                    await cursor.execute(f"""
                        UPDATE
                            colors
                        SET
                            {vote_type} = {vote_type} + 1,
                            {previous_vote} = {previous_vote} - 1
                        WHERE
                            submission_id = ?
                    """, [self.list[self.index][1]])

            else:
                await cursor.execute("""
                    INSERT INTO
                        color_votes (user_id, submission_id, vote)
                    VALUES
                        (?, ?, ?)

                """, [interaction.user.id, self.list[self.index][1], vote])

                await cursor.execute(f"""
                    UPDATE
                        colors
                    SET
                        {vote_type} = {vote_type} + 1
                    WHERE
                        submission_id = ?
                """, [self.list[self.index][1]])
            
            new_list = []
            for object in self.list:
                await cursor.execute("""
                    SELECT
                        colors.*, colors.upvotes - colors.downvotes AS score
                    FROM
                        colors
                    WHERE
                        colors.submission_id = ?
                """, [object[1]])
                new_object = await cursor.fetchone()
                new_list.append(new_object)

            self.list = new_list

        await self.update_embed(interaction)

    async def update_embed(self, interaction: discord.Interaction):
        tag_list = ""
        ic_account = "Not linked"

        async with self.client.connection.cursor() as cursor:
            await cursor.execute("""
                SELECT
                    tags.*
                FROM
                    tags
                INNER JOIN
                    color_tags
                ON
                    color_tags.submission_id = ?
                AND
                    tags.tag_id = color_tags.tag_id
            """, [self.list[self.index][1]])

            all_tags = await cursor.fetchall()

            await cursor.execute("""
                SELECT 
                    ic_id
                FROM 
                    accounts
                WHERE
                    discord_id = ?
            """, [self.list[self.index][0]])

            ic = await cursor.fetchone()

        if len(all_tags):
            tag_list = "` ".join(f"` {tag[1]} " for tag in all_tags) + "`\n\n"

        if len(ic):
            ic_account = await self.client.ic.get_details_for_user(user_id=ic[0])

        embed = discord.Embed(
            title=self.list[self.index][6] + " - " + hex(self.list[self.index][2]).replace("0x", "#"),
            timestamp=datetime.datetime.now(),
            color=discord.Color.orange(),#discord.Color.from_str(hex(self.list[self.index][2])),
            description= f"tags: {tag_list}"
        )
        embed.set_footer(text = f"Page {self.index + 1}/{len(self.list)}, 👍{self.list[self.index][3]} 👎{self.list[self.index][4]}")
        embed.add_field(name="Color Information", value=f"> ` Author    ` {await self.client.fetch_user(self.list[self.index][0])}\n> ` Author IC ` {ic_account}\n> ` Submitted ` <t:{round(self.list[self.index][5] / 1000.0)}:R>\n> ` Score     ` {self.list[self.index][7]}")

        # 201x1200
        RGBint = self.list[self.index][2]

        # int to rgb tuple conversion
        color =  ((RGBint >> 16) & 255, (RGBint >> 8) & 255, RGBint & 255)

        img = Image.new('RGB', (1200, 200), color)
        
        fp = BytesIO()
        img.save(fp, "PNG")
        fp.seek(0)

        file = discord.File(fp, filename="color.png")
        embed.set_image(url="attachment://color.png")

        await interaction.response.edit_message(embed=embed, attachments=[file], view=self)

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

        await interaction.followup.edit_message(interaction.message.id, embed=embed, view=self)

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

        await interaction.followup.edit_message(interaction.message.id, embed=embed, view=self)

class Search(commands.GroupCog, group_name="search"):

    def __init__(self, client: MyClient) -> None:
        self.client = client
        super().__init__()

    @app_commands.command(name="users", description="Search for IC users.")
    @app_commands.describe(query="Name to search for.",
        offset="Which index to start the search at (defaults to 0).",
        page="Page to start the search at (defaults to 0 i.e. the first one)."
    )
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
    @app_commands.describe(mode = "Game mode.", query="Name to search for.",
        offset="Which index to start the search at (defaults to 0).",
        page="Page to start the search at (defaults to 0 i.e. the first one)."
    )
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

        mode = ["Simulation", "Traffic Controller", "Miscellaneous"][mode - 1]
        embed.add_field(name="Map", value=f"> ` Game mode ` {mode}\n> ` Version   ` {map.map_version}\n> ` Created   ` <t:{round(map.created / 1000.0)}:R>\n> ` Updated   ` <t:{round(map.updated / 1000.0)}:R>")
        embed.add_field(name="User", value=f"> ` Nickname   ` {map.author_name}\n> ` ID         ` {map.author}\n> ` Last login ` <t:{round((await map.get_author()).last_login / 1000.0)}:R>\n> ` Discord    ` {user}")
        embed.set_image(url="https://media.discordapp.net/attachments/879324217462632478/1046064114558062683/help.png")
        embed.set_footer(text = f"Page 1/{len(maps)}, 👍{map.votes_up} 👎{map.votes_down} ❤️{map.favorites}")

        await interaction.followup.send(embed=embed, view=MapNavigation(self.client, maps, offset))

    @app_commands.command(name="colors", description="Search for colors in the hex color database.")
    @app_commands.choices(order = [
        app_commands.Choice(name="Top", value="top"),
        app_commands.Choice(name="New", value="new")
    ])
    @app_commands.describe(order="In what order to return the search results.", 
        tags="Tags to search for (separated by spaces).",
        offset="Which index to start the search at (defaults to 0).",
        user="The user whose colors to search for."
    )
    async def colors(self, interaction: discord.Interaction, order: str, tags: str = None, user: discord.User = None, offset: int = 0):
        async with self.client.connection.cursor() as cursor:
            user_query = "" if not user else f"AND colors.user_id = {user.id}"
            if tags:
                await cursor.execute(f"""
                    SELECT 
                        colors.*, colors.upvotes - colors.downvotes AS score
                    FROM 
                        colors
                    INNER JOIN 
                        tags
                    ON
                        tags.tag_name IN (?{"".join(", ?" for _ in range(len(tags.split(" ")) - 1))})
                    INNER JOIN
                        color_tags
                    ON
                        color_tags.submission_id = colors.submission_id
                    AND
                        tags.tag_id = color_tags.tag_id
                    {user_query}
                    GROUP BY
                        colors.submission_id
                    HAVING
                        COUNT(colors.submission_id)={len(tags.split(" "))}
                    ORDER BY 
                        """ + {"top": "score", "new": "created"}[order] + """ DESC
                """, tags.split(" "))

            else:
                await cursor.execute(f"""
                    SELECT
                        *, upvotes - downvotes AS score
                    FROM 
                        colors
                    {user_query.replace("AND", "WHERE")}
                    ORDER BY
                        """ + {"top": "score", "new": "created"}[order] + """ DESC
                """)

            data = await cursor.fetchall()

        if not data:
            await interaction.response.send_message("No such color found.", ephemeral=True)
            return

        if len(data) <= offset:
            offset = len(data) - 1

        tag_list = ""
        ic_account = "Not linked"

        async with self.client.connection.cursor() as cursor:
            await cursor.execute("""
                SELECT
                    tags.*
                FROM
                    tags
                INNER JOIN
                    color_tags
                ON
                    color_tags.submission_id = ?
                AND
                    tags.tag_id = color_tags.tag_id
            """, [data[offset][1]])

            all_tags = await cursor.fetchall()

            await cursor.execute("""
                SELECT 
                    ic_id
                FROM 
                    accounts
                WHERE
                    discord_id = ?
            """, [data[offset][0]])

            ic = await cursor.fetchone()

        if len(all_tags):
            tag_list = "` ".join(f"` {tag[1]} " for tag in all_tags) + "`\n\n"

        if ic:
            ic_account = await self.client.ic.get_details_for_user(user_id=ic[0])

        embed = discord.Embed(
            title=data[offset][6] + " - " + hex(data[offset][2]).replace("0x", "#"),
            timestamp=datetime.datetime.now(),
            color=discord.Color.orange(),#discord.Color.from_str(hex(data[offset][2])),
            description = f"tags: {tag_list}"
        )
        embed.set_footer(text = f"Page {offset + 1}/{len(data)}, 👍{data[offset][3]} 👎{data[offset][4]}")
        embed.add_field(name="Color Information", value=f"> ` Author    ` {await self.client.fetch_user(data[offset][0])}\n> ` Author IC ` {ic_account}\n> ` Submitted ` <t:{round(data[offset][5] / 1000.0)}:R>\n> ` Score     ` {data[offset][7]}")

        RGBint = data[offset][2]

        # int to rgb tuple conversion
        color =  ((RGBint >> 16) & 255, (RGBint >> 8) & 255, RGBint & 255)

        img = Image.new('RGB', (1200, 200), color)
        
        fp = BytesIO()
        img.save(fp, "PNG")
        fp.seek(0)

        file = discord.File(fp, filename="color.png")
        embed.set_image(url="attachment://color.png")

        await interaction.response.send_message(embed=embed, file=file, view=ColorNavigation(self.client, data, offset))

async def setup(client: commands.Bot):
    if client.debug:
        await client.add_cog(Search(client), guilds=[discord.Object(id=744653826799435806)])
    else:
        await client.add_cog(Search(client))