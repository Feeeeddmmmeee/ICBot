import discord
import datetime
import random
import json
import os
import traceback
import sys
import asyncio
import requests
from itertools import cycle
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, MissingPermissions
import ast

client = commands.Bot(command_prefix = ['ic ', 'IC ', 'Ic ', 'iC '], intents = discord.Intents.all())
token = open("token.txt", "r")
client.remove_command('help')
client.owner_id = 585115156757872653

for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
        if not filename.startswith('redditripoff'):
            client.load_extension(f'commands.{filename[:-3]}')

@client.event
async def on_ready():
    activity = discord.Activity(name="Intersection Controller", type=discord.ActivityType.playing)
    await client.change_presence(status=discord.Status.online, activity=activity)
    print('Bot is ready')

@client.event
async def on_command_error(ctx, error):
    cross = client.get_emoji(798573872916070470)
    if isinstance(error, commands.errors.MissingPermissions):
        await ctx.send(f"{cross} You don't have enough permissions to run this command!")
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send(f'{cross} Please pass in all required arguments!')
    elif isinstance(error, commands.errors.CommandOnCooldown):
        await ctx.send(f'{cross} Please wait before using this command again!')
    elif isinstance(error, commands.errors.NotOwner):
        await ctx.send(f'{cross} Only the bot owner can run this command!')
    elif isinstance(error, commands.errors.CheckFailure):
        await ctx.send(f'{cross} Seems like you were banned from using this command!')
    else:
        # All other Errors not returned come here. And we can just print the default TraceBack.
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def sort():
    with open('accounts.json', 'r') as f:
        accounts = json.load(f)

    sortedAccounts = sorted(accounts.items(), key=lambda k: requests.get(f"https://tl3.shadowtree-software.se/TL3BackEnd/rest/user2/public/info/{k[1]}", verify=False).json()["followers"], reverse=True)

    #tuple to dict here
    accounts = dict((x, y) for x, y in sortedAccounts)

    with open('accounts.json', 'w') as f:
        json.dump(accounts, f, indent=4)

@commands.is_owner()
@client.command()
async def validate(ctx, id=None):
    tick = client.get_emoji(798573863184236574)
    if id == None:
        id = ctx.guild.id

    with open("config.json", "r") as f:
        config = json.load(f)

    if int(id) in config["validIds"]:
        config["validIds"].pop(config["validIds"].index(int(id)))

        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)

        await ctx.send(f"{tick} Successfully deleted a server with the given ID ({id}) from the valid server list.")
    else:
        config["validIds"].append(int(id))

        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)

        await ctx.send(f"{tick} Successfully validated a server with the given ID ({id}).")

@client.command(aliases=["id"])
async def id_search(ctx, id):
    cross = client.get_emoji(798573872916070470)
    async with ctx.typing():
        response = requests.get(f"https://tl3.shadowtree-software.se/TL3BackEnd/rest/user2/public/info/{id}", verify = False)
    api = response.json()
    
    if not(len(api)):
        await ctx.send(f"{cross} We couldn't find any users with this ID!")
        return

    else:

        icname = api['name']
        icfollowers = api['followers']
        iclastlogin = api['lastLogin']
        icmaps = api['maps']
        icid = api['objectId']

        embed = discord.Embed(
            colour=discord.Colour.from_rgb(66, 135, 245),
            title=f"User info for `{id}`",
            timestamp=ctx.message.created_at
            )
        embed.add_field(name='Stats', value=f'Nickname: {icname}\nID: {icid}\nFollowers: {icfollowers}\nLast login: {datetime.datetime.fromtimestamp(round(iclastlogin/1000.0))}\nAmount of maps: {icmaps}', inline=False)
        embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

@client.command()
async def botinfo(ctx):
    embed=discord.Embed(
        colour=discord.Colour.from_rgb(66, 135, 245),
        description="Intersection Controller is a Discord bot which uses IC's API to connect to the game and give you some cool info!",
        timestamp=ctx.message.created_at
    )
    embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
    embed.set_author(name="Intersection Controller#2844", icon_url="https://images-ext-1.discordapp.net/external/nip0KygSdkm20jZ2Hk4EbYhipIec7Y3NSn2qhI4Wdag/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/747892846178336868/f545eae8afba55f97f3924c4cadd3355.webp?width=676&height=676")
    embed.add_field(name="Developer:", value="Feeeeddmmmeee#7784")
    embed.add_field(name="Helper", value="rnggadosen._#8546")
    await ctx.send(embed=embed)    

@client.command()
async def search(ctx, *, name):
    cross = client.get_emoji(798573872916070470)
    async with ctx.typing():
        response = requests.get(f"https://tl3.shadowtree-software.se/TL3BackEnd/rest/user2/public/search?query={name.replace(' ', '%20')}", verify = False)
    api = response.json()
    
    if not(len(api)):
        await ctx.send(f"{cross} We couldn't find any users with this name!")
        return

    else:

        embed = discord.Embed(
        colour=discord.Colour.from_rgb(66, 135, 245),
        title=f"Results of searching `{name}`:",
        timestamp=ctx.message.created_at
        )
        for item in api:
            async with ctx.typing():
                response = requests.get(f"https://tl3.shadowtree-software.se/TL3BackEnd/rest/user2/public/info/{item['objectId']}", verify = False)
            api = response.json()
            embed.add_field(name=api['name'], value=f"Followers: {api['followers']} | ID: {api['objectId']}", inline=False)
                
        embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


@client.command()
async def profile(ctx, *, name):
    cross = client.get_emoji(798573872916070470)
    async with ctx.typing():
        response = requests.get(f"https://tl3.shadowtree-software.se/TL3BackEnd/rest/user2/public/search?query={name.replace(' ', '%20')}", verify = False)
    api = response.json()
    i = 0

    if not(len(api)):
        await ctx.send(f"{cross} We couldn't find any users with this name!")
        return

    else:
        while(i<=len(api)):
            if api[i]['name'] == name:
                async with ctx.typing():
                    response = requests.get(f"https://tl3.shadowtree-software.se/TL3BackEnd/rest/user2/public/info/{api[i]['objectId']}", verify = False)
                api = response.json()
                icname = api['name']
                icfollowers = api['followers']
                iclastlogin = api['lastLogin']
                icmaps = api['maps']
                icid = api['objectId']

                embed = discord.Embed(
                colour=discord.Colour.from_rgb(66, 135, 245),
                title=f"Profile of `{icname}`",
                timestamp=ctx.message.created_at
                )
                embed.add_field(name='Stats', value=f'Nickname: {icname}\nID: {icid}\nFollowers: {icfollowers}\nLast login: {datetime.datetime.fromtimestamp(round(iclastlogin/1000.0))}\nAmount of maps: {icmaps}', inline=False)
                #embed.add_field(name='ID:', value=f'{icid}', inline=False)
                #embed.add_field(name=f'Followers:', value=f'{icfollowers}', inline=False)
                #embed.add_field(name='Last login:', value=f'{datetime.datetime.fromtimestamp(round(iclastlogin/1000.0))}', inline=False)
                #embed.add_field(name='Amount of maps:', value=f'{icmaps}', inline=False)
                embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)

                await ctx.send(embed=embed)
                i = i + 1
            else:
                i = i + 1

@client.command()
async def list(ctx, mode):
    cross = client.get_emoji(798573872916070470)
    if mode.lower() == "tc":
        x = '2'
    elif mode.lower() == "sim":
        x = '1'
    elif mode.lower() == "misc":
        x = '3'
    else:
        await ctx.send(f'{cross} Please enter a valid mode!')
        return

    async with ctx.typing():
        response = requests.get("https://tl3.shadowtree-software.se/TL3BackEnd/rest/map/public/top/" + x +"/day?maxversion=999&trendsystem=1", verify = False)
    api = response.json()

    embed = discord.Embed(
    colour=discord.Colour.from_rgb(66, 135, 245),
    title=f"Today's list of top 12 maps:",
    timestamp=ctx.message.created_at
    )
    for item in api:
        embed.add_field(name=item['name'], value=f"By {item['authorName']} | {item['votesUp']} likes, {item['votesDown']} dislikes, {item['favorites']} favorites", inline=False)

    embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)

    await ctx.send(embed=embed)

@client.command()
async def trending(ctx, mode):
    cross = client.get_emoji(798573872916070470)
    if mode.lower() == "tc":
        x = '2'
    elif mode.lower() == "sim":
        x = '1'
    elif mode.lower() == "misc":
        x = '3'
    else:
        await ctx.send(f'{cross} Please enter a valid mode!')
        return

    async with ctx.typing():
        response = requests.get("https://tl3.shadowtree-software.se/TL3BackEnd/rest/map/public/top/" + x +"/day?maxversion=999&trendsystem=1", verify = False)
    api = response.json()

    embed = discord.Embed(
    colour=discord.Colour.from_rgb(66, 135, 245),
    title=f"Today's first map in the trending category:",
    timestamp=ctx.message.created_at
    )
    embed.add_field(name='Name', value=api[0]['name'], inline=False)
    embed.add_field(name='Author', value=api[0]['authorName'], inline=False)
    embed.add_field(name='Description', value=api[0]['desc'], inline=False)
    embed.add_field(name='Likes', value=api[0]['votesUp'], inline=False)
    embed.add_field(name='Dislikes', value=api[0]['votesDown'], inline=False)
    embed.add_field(name='Favorites', value=api[0]['favorites'], inline=False)
    embed.add_field(name='Map Version', value=api[0]['mapVersion'], inline=False)
    embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@client.command()
async def help(ctx):
    embed = discord.Embed(
        colour=discord.Colour.from_rgb(66, 135, 245),
        title=f'Need some help?',
        timestamp=ctx.message.created_at
    )
    embed.add_field(name='Userinfo', value='Gets user info from a mention! required arguments: `ic userinfo <@mention>` (requires a linked account)', inline=False)
    embed.add_field(name='Link', value='Links a IC account to a Discord account (admin only)', inline=False)
    embed.add_field(name='Unlink', value='Unlinks a IC account from a Discord account (admin only)', inline=False)
    embed.add_field(name='Rank', value='Shows your current rank and level (depending on in-game followers)', inline=False)
    embed.add_field(name='Ban', value='Banned users can no longer use `ic suggest` (admin only)', inline=False)
    embed.add_field(name='Unban', value='Unbans a user (admin only)', inline=False)
    embed.add_field(name='Search', value='Searches for users', inline=False)
    embed.add_field(name='Id', value='Gets a profile of a user with a given ID', inline=False)
    embed.add_field(name='Profile', value='Checks a profile of a user', inline=False)
    embed.add_field(name='Trending', value="Shows the map which is currenly first in the trending category! required arguments: `ic trending <sim>/<tc>/<misc>`", inline=False)
    embed.add_field(name='List', value="Shows a list of top 12 maps from the trending category! required arguments: `ic list <sim>/<tc>/<misc>`")
    embed.add_field(name='Suggest', value='Suggest a new feature to the Dev! it will be posted in <#600465489508171776>', inline=False)
    embed.add_field(name='Verify', value='Verify a new user! required arguments: `ic verify <@mention> <id>` (admin-only)', inline=False)
    embed.add_field(name='Bypass', value='Bypasses a user. Bypassing is the same as verifying but it does not link accounts (admin only)', inline=False)
    embed.add_field(name="Outsider", value=' Its the same as verify but for outsiders which means that instead of the `IC player` role it will give the mentioned user the `outsider :(` role', inline=False)
    embed.add_field(name='Botinfo', value='Shows some info about the bot', inline=False)
    embed.add_field(name='Rules', value='Checks a specified server rule. reqired argments: `ic rules <number>`', inline=False)
    embed.add_field(name='Ping', value="Checks the client's latency", inline=False)
    embed.add_field(name='Cheats', value='Shows all the cheats', inline=False)
    embed.add_field(name='Host', value='Submits a competition', inline=False)
    embed.add_field(name='Submit', value='Adds your submission for a competition', inline=False)
    embed.add_field(name='Voting', value='Starts a voting for competition submissions', inline=False)
    embed.add_field(name='End', value='Ends a competition, announces the winner', inline=False)
    embed.add_field(name='Approve', value='Approves a submitted competition (admin only)', inline=False)
    embed.add_field(name='Competition', value='Checks info on a competition', inline=False)
    embed.add_field(name='Update', value='Updates one of the rules (admin only)', inline=False)
    embed.add_field(name='Data', value="A more complicated command so I won't explain it here. Dm me if you want.", inline=False)
    embed.add_field(name='Maps', value="A command used to get users' maps. Required arguments `ic maps <user id> <how far the map is from the first one>` (0 is the newest)", inline=False)
    embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)

    await ctx.send(embed=embed)
    

@client.command()
async def ping(ctx):
    embed = discord.Embed(
        colour=discord.Colour.from_rgb(66, 135, 245),
        title=f'Pong! {round(client.latency * 1000)}ms',
        timestamp=ctx.message.created_at
    )
    embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
'''
@client.command()
@has_permissions(administrator=True)
async def verify(ctx, member : discord.Member, *, nick):
    guild = ctx.guild
    chance=random.randint(0, 100)
    if chance < 5:
        response=f'{member.mention} **just got Intersection Controlled!**'
    else:
        response=f'**An administrator has successfully verified** {member.mention}**!**'

    for role in guild.roles:
        if role.name == 'IC player':
            await member.add_roles(role)
    for role in guild.roles:
        if role.name == 'Unverified':
            await member.remove_roles(role)
    embed = discord.Embed(
        colour=discord.Colour.from_rgb(66, 135, 245),
        description=response,
        timestamp=ctx.message.created_at
    )
    embed.set_footer(text=f'Verified by {ctx.author}', icon_url=ctx.author.avatar_url)
    await ctx.channel.purge(limit=1)
    await member.edit(nick=nick)
    await ctx.send(embed=embed)'''

@client.command()
async def cheats(ctx):
    embed = discord.Embed(
        colour=discord.Colour.from_rgb(66, 135, 245),
        title='Here are the current "cheats" which will not break the game:',
        description='\n\n**Fps** - Displays an FPS counter.\n\n**RegnarDet?** - Forces the weather to rain.\n\n**TorsVrede** - Forces the weather to thunderstorm.\n\n**Solkatt** - Forces the weather to sunny.\n\n**Dimfilt** - Forces the weather to fog.\n\n**Väderlek or Vaderlek** - Sets the weather to the default dynamic setting.\n\n**Händelser or Handelser** - Random events are triggered as often as possible.\n\n**Ögonsten or Ogonsten** - Graphics settings not lowered when zooming out.\n\n**GömdaSaker or GomdaSaker** - Unlocks all decorative objects.\n\n**Uppdatera** - Opens the update link for your installation ([shadowtree.se](https://shadowtree-software.se/tr3/lanes3.apk) / [Google Play](https://play.google.com/store/apps/details?id=se.shadowtree.software.trafficbuilder) / [Amazon](https://www.amazon.com/gp/mas/dl/android?p=se.shadowtree.software.trafficbuilder))\n\n**Blindstyre** - Disables vehicles stopping before crashed vehicles.',
        timestamp=ctx.message.created_at
    )
    embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)

def readJson(name):
    with open(name, "r") as f: return json.load(f)

def writeJson(var, name):
    with open(name, "w") as f: json.dump(var, f, indent=4)

@commands.is_owner()
@client.command()
async def ev(ctx, *, cmd):
    """Evaluates input.
    Input is interpreted as newline seperated statements.
    If the last statement is an expression, that is the return value.
    Usable globals:
      - `bot`: the bot instance
      - `discord`: the discord module
      - `commands`: the discord.ext.commands module
      - `ctx`: the invokation context
      - `__import__`: the builtin `__import__` function
    Such that `>eval 1 + 1` gives `2` as the result.
    The following invokation will cause the bot to send the text '9'
    to the channel of invokation and return '3' as the result of evaluating
    >eval ```
    a = 1 + 2
    b = a * 2
    await ctx.send(a + b)
    a
    ```
    """
    fn_name = "_eval_expr"

    cmd = cmd.strip("` ")

    # add a layer of indentation
    cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

    # wrap in async def body
    body = f"async def {fn_name}():\n{cmd}"

    parsed = ast.parse(body)
    body = parsed.body[0].body

    insert_returns(body)

    env = {
        'bot': ctx.bot,
        'discord': discord,
        'commands': commands,
        'ctx': ctx,
        '__import__': __import__,
        'json': json,
        'requests': requests,
        'client': client,
        'readJson': readJson,
        'writeJson': writeJson,
    }
    exec(compile(parsed, filename="<ast>", mode="exec"), env)

    result = (await eval(f"{fn_name}()", env))
    await ctx.send(result)
    print('Eval succeeded!')

client.run(token.read())