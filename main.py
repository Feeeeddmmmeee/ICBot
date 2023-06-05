import discord
from discord.ext import commands, tasks

from colorlog import ColoredFormatter
from dotenv import load_dotenv
from typing import List
import logging
import os
import asyncio
import aiosqlite
import aiohttp

import tl3api

# getting the default discord logger
logger = logging.getLogger("discord")

# getting environment variables
load_dotenv(dotenv_path = r"./config/config.env")
TOKEN = os.getenv("TOKEN") 
DEBUG = bool(os.getenv("DEBUG"))

# creating the client
class MyClient(commands.Bot):
    debug: bool
    connection: aiosqlite.Connection
    session: aiohttp.ClientSession
    ic: tl3api.Client

    def __init__(self, debug, *args, **kwargs):
        self.debug = debug
        super().__init__(*args, **kwargs)

    async def setup_hook(self):
        self.owner_id = 585115156757872653
        self.connection = await aiosqlite.connect("database.db")
        logger.info("Established connection to database")

        with open("schema.sql") as schema:
            await self.connection.executescript(schema.read())

        logger.info("Ran schema.sql")

        self.session = aiohttp.ClientSession()
        self.ic = tl3api.Client(self.session)
        logger.info("Initialized the IC API client")

    async def close(self):
        await self.connection.close()
        await self.ic.close()
        return await super().close()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = MyClient(DEBUG, command_prefix = commands.when_mentioned_or(""), help_command = None, intents = intents)

def get_index(followers: int):
    for i, f in enumerate([1000, 500, 200, 100, 50, 10, 0]):
        if followers >= f: return 6 - i

async def update_member_roles(followers: int, member: discord.Member, roles: List[discord.Role]):
    index = get_index(followers)

    roles_to_remove = roles.copy()
    roles_to_remove.pop(index)

    edit = [role for role in member.roles if role not in roles_to_remove]
    if not roles[index] in edit: edit.append(roles[index])
    await member.edit(roles=edit)

async def update_member(member: discord.Member, client, roles: List[discord.Role]):
    logger.debug(f"Starting task for {member}")
    
    async with client.connection.cursor() as cursor:
        await cursor.execute(f"SELECT ic_id FROM accounts WHERE discord_id = {member.id}")
        data = await cursor.fetchone()

    if data:
        followers = (await client.ic.get_details_for_user(user_id=data[0])).followers
        await update_member_roles(followers, member, roles)

    logger.debug(f"Finished task for {member}")

@tasks.loop(seconds=30)
async def update_roles(client: MyClient):
    logger.debug(f"Starting loop")
    guild = client.get_guild(744653826799435806 if DEBUG else 469861886960205824)
    roles = [discord.utils.get(guild.roles, name=(["Newbie (Below 10 Followers)"] + [f + "+ Followers" for f in ['10', '50', '100', '200', '500', '1000']])[i]) for i in range(7)]
    tasks = []
    
    # Create task for each user
    for member in guild.members:
        tasks.append(asyncio.create_task(update_member(member, client, roles)))
    
    # Wait until all tasks are finished
    for task in tasks:
        await task

    logger.debug(f"Finished loop")

@client.command(aliases = ["s"])
@commands.is_owner()
async def sync(ctx: commands.Context):
    if client.debug:
        fmt = await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"{len(fmt)} commands synced locally!")
    else:
        fmt = await ctx.bot.tree.sync()
        await ctx.send(f"{len(fmt)} commands synced globally!")

@client.command(aliases = ["r"])
@commands.is_owner()
async def refresh(ctx: commands.Context):
    loaded, unloaded = 0, 0
    for dir in os.listdir("./cogs"):
        for filename in os.listdir(f"./cogs/{dir}"):
            if filename.endswith(".py"):
                try:
                    await client.unload_extension(f"cogs.{dir}.{filename[:-3]}")
                    logger.debug(f"Unloaded cogs.{dir}.{filename[:-3]}")
                    unloaded += 1
                except:
                    logger.warning(f"Failed to unload extension cogs.{dir}.{filename[:-3]}")
                await client.load_extension(f"cogs.{dir}.{filename[:-3]}")
                logger.debug(f"Loaded cogs.{dir}.{filename[:-3]}")
                loaded += 1

    logger.info(f"{unloaded} extensions unloaded, {loaded} extensions loaded ({loaded - unloaded} new)")
    await ctx.send(f"{unloaded} extensions unloaded, {loaded} extensions loaded ({loaded - unloaded} new)")

async def main():
    # setting up a custom logger
    date_format = "%Y-%m-%d %H:%M:%S"

    if client.debug: 
        logger.setLevel(logging.DEBUG)
    else: 
        logger.setLevel(logging.INFO)

    #logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    formatter = ColoredFormatter("{log_color}[{asctime}] [{levelname}] {name}: {message}", datefmt = date_format, style = "{", log_colors={"INFO": "blue", "WARNING": "yellow", "ERROR": "red", "CRITICAL": "red"})

    #handler = logging.FileHandler(filename = "discord.log", encoding = "utf-8", mode = "w")
    #formatter = logging.Formatter("[{asctime}] [{levelname}] {name}: {message}", datefmt = date_format, style = "{")

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # loading commands
    for dir in os.listdir("./cogs"):
        for filename in os.listdir(f"./cogs/{dir}"):
            if(filename.endswith(".py")):
                await client.load_extension(f"cogs.{dir}.{filename[:-3]}")
                logger.debug(f"Loaded cogs.{dir}.{filename[:-3]}")

    await client.start(TOKEN)

if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        logger.info("Stopping the bot")
        asyncio.run(client.close())
