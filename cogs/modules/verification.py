import discord
from discord.ext import commands
from discord import app_commands

from main import logger, MyClient

import tl3api

import time
import string
import random
import asyncio

def generate_code(length: int = 6):
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for i in range(length))

async def verify(user: tl3api.User, interaction: discord.Interaction, client: commands.Bot):
    code = generate_code(4)
    
    if user.maps:
        map = (await user.get_user_maps())[0]
        embed = discord.Embed(
            color=discord.Color.orange(),
            description=f"In order to prove you actually own the selected account you will be required to post a comment on your most recently uploaded map - **{map}**. The comment must only contain the 4-character code sent in my next message. Once you're done your account will be linked."
        )
        embed.set_author(name=f"Account Verification - {user}", icon_url=client.user.display_avatar.url)

        await interaction.followup.send(embed=embed, ephemeral=True)
        await interaction.followup.send(code, ephemeral=True)

        for i in range(10):
            await asyncio.sleep(15)

            try: comment = (await map.get_comments(limit=1))[0]
            except: pass

            if comment.comment == code and comment.user == user.object_id:
                break

        try: 
            if comment.comment == code and comment.user == user.object_id:
                async with client.connection.cursor() as cursor:
                    await cursor.execute("SELECT ic_id FROM accounts WHERE discord_id = ?", [interaction.user.id])
                    data = await cursor.fetchone()

                    timestamp = round(time.time() * 1000)

                    if data:
                        await cursor.execute("UPDATE accounts SET ic_id = ?, linked_at = ? WHERE discord_id = ?", [user.object_id, timestamp, interaction.user.id])
                        logger.debug(f"Account for user {interaction.user} updated")
                    else:
                        await cursor.execute("INSERT INTO accounts(discord_id, ic_id, linked_at) VALUES(?, ?, ?)", [interaction.user.id, user.object_id, timestamp])
                        logger.debug(f"Linked account for user {interaction.user}")
                                
                    await client.connection.commit()

                    await cursor.execute(f"SELECT * FROM accounts")
                    data = await cursor.fetchall()

                activity = discord.Activity(name=f"{len(data)} Linked Accounts", type=discord.ActivityType.watching)
                await client.change_presence(status=discord.Status.idle, activity=activity)

                await interaction.followup.send("Account successfully linked.", ephemeral=True)

            else:
                await interaction.followup.send("Verification failed.", ephemeral=True)

        except:
            await interaction.followup.send("Verification failed.", ephemeral=True)
            
    else:
        embed = discord.Embed(
            color=discord.Color.orange(),
            description=f"In order to prove you actually own the selected account you will be required to upload a new map on your account. The map name must only contain the 4-character code sent in my next message. Once you're done your account will be linked."
        )
        embed.set_author(name=f"Account Verification - {user}", icon_url=client.user.display_avatar.url)

        await interaction.followup.send(embed=embed, ephemeral=True)
        await interaction.followup.send(code, ephemeral=True)

        for i in range(20):
            await asyncio.sleep(15)

            try: 
                map = (await user.get_user_maps())[0]
                if map.name == code:
                    break
            except: pass

        try:
            if map.name == code:
                async with client.connection.cursor() as cursor:
                    await cursor.execute("SELECT ic_id FROM accounts WHERE discord_id = ?", [interaction.user.id])
                    data = await cursor.fetchone()

                    timestamp = round(time.time() * 1000)

                    if data:
                        await cursor.execute("UPDATE accounts SET ic_id = ?, linked_at = ? WHERE discord_id = ?", [user.object_id, timestamp, interaction.user.id])
                        logger.debug(f"Account for user {interaction.user} updated")
                    else:
                        await cursor.execute("INSERT INTO accounts(discord_id, ic_id, linked_at) VALUES(?, ?, ?)", [interaction.user.id, user.object_id, timestamp])
                        logger.debug(f"Linked account for user {interaction.user}")
                                
                    await client.connection.commit()

                    await cursor.execute(f"SELECT * FROM accounts")
                    data = await cursor.fetchall()

                activity = discord.Activity(name=f"{len(data)} Linked Accounts", type=discord.ActivityType.watching)
                await client.change_presence(status=discord.Status.idle, activity=activity)

                await interaction.followup.send("Account successfully linked.", ephemeral=True)

            else:
                await interaction.followup.send("Verification failed.", ephemeral=True)

        except:
            await interaction.followup.send("Verification failed.", ephemeral=True)

class Confirmation(discord.ui.View):
    def __init__(self, client: commands.Bot, user: tl3api.User, *, timeout = 60):
        self.client = client
        self.user = user
        super().__init__(timeout=timeout)

    @discord.ui.button(label="Select", style=discord.ButtonStyle.success)
    async def select(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.cancel.disabled = True
        self.select.disabled = True
        await interaction.response.defer()
        await interaction.edit_original_response(view=self)

        await verify(self.user, interaction, self.client)

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.cancel.disabled = True
        self.select.disabled = True
        await interaction.response.defer()
        await interaction.edit_original_response(view=self)
        await interaction.followup.send("I have stopped the verification process. Use /verify again if you wish to restart.", ephemeral=True)

class Navigation(discord.ui.View):
    def __init__(self, client: MyClient, query: str, index: int = 0, *, timeout = 120):
        self.client = client
        self.index = index
        self.query = query
        super().__init__(timeout=timeout)

    async def update_embed(self, interaction: discord.Interaction):
        latest_map = ""

        try:
            ic_account = (await self.client.ic.search_for_users(query=self.query, result=1, page=self.index))[0]
        except:
            self.index -= 1
            ic_account = (await self.client.ic.search_for_users(query=self.query, result=1, page=self.index))[0]

        try:
            latest_map = f"> ` Latest map ` {(await ic_account.get_user_maps())[0]}\n"
        except:
            pass

        embed = discord.Embed(
            color=discord.Color.orange(),
            description=f"> ` Followers  ` {ic_account.followers}\n> ` ID         ` {ic_account.object_id}\n" + latest_map + f"> ` Maps       ` {ic_account.maps}"
        )
        embed.set_author(name=ic_account)
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(emoji="<:arrow:1046081153737687080>", style=discord.ButtonStyle.grey)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index -= 1
        if self.index < 0: self.index = 0
        await self.update_embed(interaction)

    @discord.ui.button(label="Select", style=discord.ButtonStyle.success)
    async def select(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.previous.disabled = True
        self.select.disabled = True
        self.next.disabled = True
        await interaction.response.defer()
        await interaction.edit_original_response(view=self)
        await verify((await self.client.ic.search_for_users(query=self.query, result=1, page=self.index))[0], interaction, self.client)

    @discord.ui.button(emoji="<:arrowR:1046384022726656040>", style=discord.ButtonStyle.grey)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index += 1
        await self.update_embed(interaction)

class Modal(discord.ui.Modal, title="Account Verification"):
    input = discord.ui.TextInput(label="placeholder")
    def __init__(self, client: MyClient, name: str, *args, **kwargs):
        self.client = client
        self.input.label = name
        super().__init__(*args, **kwargs)

    async def on_submit(self, interaction: discord.Interaction):
        if self.input.label == "name":
            try:
                ic_account = (await self.client.ic.search_for_users(result=1,query=self.input))[0]
            except:
                await interaction.response.send_message("No users with such a name found.", ephemeral=True)
                return

            latest_map = ""

            try:
                latest_map = f"> ` Latest map ` {(await ic_account.get_user_maps())[0]}\n"
            except:
                pass

            embed = discord.Embed(
                color=discord.Color.orange(),
                description=f"> ` Followers  ` {ic_account.followers}\n> ` ID         ` {ic_account.object_id}\n" + latest_map + f"> ` Maps       ` {ic_account.maps}"
            )
            embed.set_author(name=ic_account)

            await interaction.response.send_message(embed=embed, view=Navigation(self.client, self.input), ephemeral=True)    

        else:
            try:
                id = int(str(self.input).replace("#", "").replace(" ", ""))
                ic_account = await self.client.ic.get_details_for_user(user_id=id)
            except:
                await interaction.response.send_message("No users with such an ID found.", ephemeral=True)
                return

            latest_map = ""

            try:
                latest_map = f"> ` Latest map ` {(await ic_account.get_user_maps())[0]}\n"
            except:
                pass

            embed = discord.Embed(
                color=discord.Color.orange(),
                description=f"> ` Followers  ` {ic_account.followers}\n> ` ID         ` {ic_account.object_id}\n" + latest_map + f"> ` Maps       ` {ic_account.maps}"
            )
            embed.set_author(name=ic_account)

            await interaction.response.send_message(embed=embed, view=Confirmation(self.client, ic_account), ephemeral=True)

class NameIDSelect(discord.ui.Select):
    def __init__(self, client: commands.Bot):
        self.client = client
        options = [
            discord.SelectOption(label="Name", description="Use your account name to find your account."),
            discord.SelectOption(label="ID", description="Use your account ID to find your account."),
        ]
        super().__init__(placeholder="Choose an option", max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "Name":
            await interaction.response.send_modal(Modal(self.client, "name"))
        else:
            await interaction.response.send_modal(Modal(self.client, "id"))

class SelectView(discord.ui.View):
    def __init__(self, client: commands.Bot, *, timeout = 60):
        super().__init__(timeout=timeout)
        self.add_item(NameIDSelect(client))

class Verify(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="verify", description="Starts the verification process.")
    async def verify(self, interaction: discord.Interaction):
        await self.verification(interaction, interaction.user)

    async def verification(self, interaction: discord.Interaction, user: discord.Member):
        embed = discord.Embed(
            color=discord.Color.orange(),
            description="Firstly you need to specify an **IC account** you want me to link your **Discord** to. To do that you'll need to provide me with either the **name** or the **ID** of your IC account. Use the select menu below to choose your preferred option."
        )
        embed.set_author(name="Account Verification", icon_url=self.client.user.display_avatar.url)
        embed.set_image(url="https://media.discordapp.net/attachments/879324217462632478/1047970480017117324/v.png")
        await interaction.response.send_message(embed=embed, view=SelectView(self.client),ephemeral=True)

async def setup(client: commands.Bot):
    if client.debug:
        await client.add_cog(Verify(client), guilds=[discord.Object(id=744653826799435806)])
    else:
        await client.add_cog(Verify(client))
