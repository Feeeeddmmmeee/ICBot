import discord
from discord.ext import commands
from discord import app_commands

from typing import Optional
from main import logger, MyClient

import time
import re

class Colors(commands.Cog):

    def __init__(self, client: MyClient):
        self.client = client

    @app_commands.command(name="submit", description="Submit a color to the hex database.")
    @app_commands.describe(color = "The hex code of your color submission.")
    @app_commands.describe(tags="A list of tags you want to add to your color. (Separated by spaces, no more than 10 tags can be added, only lowercase letters, numbers and underscores are allowed)")
    async def submit(self, interaction: discord.Interaction, color: str, name: str, description: str, tags: Optional[str] = None):
        await interaction.response.defer()
        color = color.replace("#", "").replace("0x", "")
        if tags: tags = tags.split(" ")

        async with self.client.connection.cursor() as cursor:
            await cursor.execute("INSERT INTO colors (user_id, color, created, name, description) VALUES(?, ?, ?, ?, ?)", 
                [interaction.user.id, int(color, 16), round(time.time() * 1000), name, description])

            submission_id = cursor.lastrowid
            await cursor.execute("INSERT INTO color_votes (user_id, submission_id, vote) VALUES(?, ?, ?)", 
                [interaction.user.id, submission_id, 1])

            if tags:
                if len(tags) > 10:
                    tags = tags[0:10]

                for tag in tags:
                    tag = tag.lower()
                    if not bool(re.match("^[a-z0-9_]*$", tag)):
                        continue

                    await cursor.execute("SELECT tag_id FROM tags WHERE tag_name = ?", [tag])
                    data = await cursor.fetchone()

                    if not data: 
                        await cursor.execute("INSERT INTO tags (tag_name) VALUES(?)", [tag])
                        tag_id = cursor.lastrowid

                    else:
                        tag_id = data[0]

                    await cursor.execute("INSERT INTO color_tags (submission_id, tag_id) VALUES(?, ?)", 
                        [submission_id, tag_id])

        await self.client.connection.commit()
        
        await interaction.followup.send("done")

async def setup(client: commands.Bot):
    if client.debug:
        await client.add_cog(Colors(client), guilds=[discord.Object(id=744653826799435806)])
    else:
        await client.add_cog(Colors(client))