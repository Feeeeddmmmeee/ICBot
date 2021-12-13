import discord, os, intersection, asyncio
from discord.ext import commands, tasks
from dotenv import load_dotenv
from libs import asqlite

intents = discord.Intents.all()
discord.member = True
discord.guild = True
discord.reaction = True

load_dotenv(dotenv_path = "./config/token.env")
TOKEN = os.getenv('TOKEN')

client = commands.Bot(command_prefix = ['ic ', 'IC ', 'Ic ', 'iC '], intents = intents, allowed_mentions=discord.AllowedMentions(everyone=False))

client.remove_command('help')
client.owner_id = 585115156757872653
guild_id = 744653826799435806 #469861886960205824

@client.before_invoke
async def typing(ctx):
    if not ctx.command.name in ['verify', 'suggest']:
        await ctx.trigger_typing()

@client.event
async def on_ready():
    print(f">> Logged in as {client.user}")

    async with asqlite.connect("database.sqlite") as conn:
        async with conn.cursor() as cursor:

            await cursor.execute(f'SELECT * FROM accounts')
            amount_of_users =  await cursor.fetchall()

    activity = discord.Activity(name=f"{len(amount_of_users)} Linked Accounts", type=discord.ActivityType.watching)
    await client.change_presence(status=discord.Status.online, activity=activity)

    follower_roles.start()

def roles(member: discord.Member, followers, guild: discord.Guild):
    less = discord.utils.get(guild.roles,name="Newbie (Below 10 Followers)")
    f10 = discord.utils.get(guild.roles,name="10+ Followers")
    f50 = discord.utils.get(guild.roles,name="50+ Followers")
    f100 = discord.utils.get(guild.roles,name="100+ Followers")
    f200 = discord.utils.get(guild.roles,name="200+ Followers")
    f500 = discord.utils.get(guild.roles,name="500+ Followers")
    f1000 = discord.utils.get(guild.roles,name="1000+ Followers")

    member_roles = member.roles

    return_var = []
    temp_add = []
    temp_remove = []

    if followers:
        if followers > 1000:
            if less in member_roles:
                temp_remove.append(less)
            if f10 in member_roles:
                temp_remove.append(f10)
            if f50 in member_roles:
                temp_remove.append(f50)
            if f100 in member_roles:
                temp_remove.append(f100)
            if f200 in member_roles:
                temp_remove.append(f200)
            if f500 in member_roles:
                temp_remove.append(f500)
            if not f1000 in member_roles:
                temp_add.append(f1000)

        elif followers > 500:
            if less in member_roles:
                temp_remove.append(less)
            if f10 in member_roles:
                temp_remove.append(f10)
            if f50 in member_roles:
                temp_remove.append(f50)
            if f100 in member_roles:
                temp_remove.append(f100)
            if f200 in member_roles:
                temp_remove.append(f200)
            if not f500 in member_roles:
                temp_add.append(f500)
            if f1000 in member_roles:
                temp_remove.append(f1000)

        elif followers > 200:
            if less in member_roles:
                temp_remove.append(less)
            if f10 in member_roles:
                temp_remove.append(f10)
            if f50 in member_roles:
                temp_remove.append(f50)
            if f100 in member_roles:
                temp_remove.append(f100)
            if not f200 in member_roles:
                temp_add.append(f200)
            if f500 in member_roles:
                temp_remove.append(f500)
            if f1000 in member_roles:
                temp_remove.append(f1000)

        elif followers > 100:
            if less in member_roles:
                temp_remove.append(less)
            if f10 in member_roles:
                temp_remove.append(f10)
            if f50 in member_roles:
                temp_remove.append(f50)
            if not f100 in member_roles:
                temp_add.append(f100)
            if f200 in member_roles:
                temp_remove.append(f200)
            if f500 in member_roles:
                temp_remove.append(f500)
            if f1000 in member_roles:
                temp_remove.append(f1000)

        elif followers > 50:
            if less in member_roles:
                temp_remove.append(less)
            if f10 in member_roles:
                temp_remove.append(f10)
            if not f50 in member_roles:
                temp_add.append(f50)
            if f100 in member_roles:
                temp_remove.append(f100)
            if f200 in member_roles:
                temp_remove.append(f200)
            if f500 in member_roles:
                temp_remove.append(f500)
            if f1000 in member_roles:
                temp_remove.append(f1000)

        elif followers > 10:
            if less in member_roles:
                temp_remove.append(less)
            if not f10 in member_roles:
                temp_add.append(f10)
            if f50 in member_roles:
                temp_remove.append(f50)
            if f100 in member_roles:
                temp_remove.append(f100)
            if f200 in member_roles:
                temp_remove.append(f200)
            if f500 in member_roles:
                temp_remove.append(f500)
            if f1000 in member_roles:
                temp_remove.append(f1000)

        else:
            if not less in member_roles:
                temp_add.append(less)
            if f10 in member_roles:
                temp_remove.append(f10)
            if f50 in member_roles:
                temp_remove.append(f50)
            if f100 in member_roles:
                temp_remove.append(f100)
            if f200 in member_roles:
                temp_remove.append(f200)
            if f500 in member_roles:
                temp_remove.append(f500)
            if f1000 in member_roles:
                temp_remove.append(f1000)

    else:
        if less in member_roles:
            temp_remove.append(less)
        if f10 in member_roles:
            temp_remove.append(f10)
        if f50 in member_roles:
            temp_remove.append(f50)
        if f100 in member_roles:
            temp_remove.append(f100)
        if f200 in member_roles:
            temp_remove.append(f200)
        if f500 in member_roles:
            temp_remove.append(f500)
        if f1000 in member_roles:
            temp_remove.append(f1000)
    
    return_var.append(temp_add)
    return_var.append(temp_remove)

    return return_var

async def update_follower_roles(member: discord.Member, guild: discord.Guild):
    async with asqlite.connect("database.sqlite") as conn:
        async with conn.cursor() as cursor:

            await cursor.execute(f'SELECT ic_id FROM accounts WHERE discord_id = {member.id}')
            id = await cursor.fetchone()
            
    if id:
        ic_user_object = intersection.user.get_details_for_user(userId=id[0])
        followers = ic_user_object.followers

        await member.add_roles(*roles(member, followers, guild)[0])
        await member.remove_roles(*roles(member, followers, guild)[1])
        
    else: 
        await member.add_roles(*roles(member, None, guild)[0])
        await member.remove_roles(*roles(member, None, guild)[1])

@tasks.loop(seconds=60)
async def follower_roles():
    guild = client.get_guild(guild_id)
    task = []

    for member in guild.members: 
        task.append(asyncio.create_task(update_follower_roles(member, guild)))

    for future in task:
        await future

for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
        client.load_extension(f'commands.{filename[:-3]}')

for filename in os.listdir('./events'):
    if filename.endswith('.py'):
        client.load_extension(f'events.{filename[:-3]}')

client.run(TOKEN)