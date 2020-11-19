import discord
import datetime
import random
import json
import os
import traceback
import sys
import asyncio
import requests
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, MissingPermissions

client = commands.Bot(command_prefix = 'ic ')
token = open("token.txt", "r")
client.remove_command('help')

for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
        client.load_extension(f'commands.{filename[:-3]}')

@client.event
async def on_ready():
    activity = discord.Activity(name="Intersection Controller", type=discord.ActivityType.playing)
    await client.change_presence(status=discord.Status.online, activity=activity)
    print('Bot is ready')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send(':warning: Please pass in all required arguments.')
    else:
        # All other Errors not returned come here. And we can just print the default TraceBack.
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

@client.command()
async def search(ctx, *, name):
    response = requests.get(f"https://tl3.shadowtree-software.se/TL3BackEnd/rest/user2/public/search?query={name.replace(' ', '%20')}", verify = False)
    api = response.json()
    
    if not(len(api)):
        await ctx.send(":warning: We couldn't find any users with this name!")
        return

    else:

        embed = discord.Embed(
        colour=discord.Colour.from_rgb(66, 135, 245),
        title=f"Results of searching `{name}`:",
        timestamp=ctx.message.created_at
        )
        for item in api:
            response = requests.get(f"https://tl3.shadowtree-software.se/TL3BackEnd/rest/user2/public/info/{item['objectId']}", verify = False)
            api = response.json()
            embed.add_field(name=api['name'], value=f"Followers: {api['followers']} | ID: {api['objectId']}", inline=False)
                
        embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)    

@client.command()
async def profile(ctx, *, name):
    response = requests.get(f"https://tl3.shadowtree-software.se/TL3BackEnd/rest/user2/public/search?query={name.replace(' ', '%20')}", verify = False)
    api = response.json()
    i = 0

    if not(len(api)):
        await ctx.send(":warning: We couldn't find any users with this name!")
        return

    else:
        while(i<=len(api)):
            if api[i]['name'] == name:
                response = requests.get(f"https://tl3.shadowtree-software.se/TL3BackEnd/rest/user2/public/info/{api[i]['objectId']}", verify = False)
                api = response.json()
                icname = api['name']
                icfollowers = api['followers']
                iclastlogin = api['lastLogin']
                icmaps = api['maps']
                icid = api['objectId']

                embed = discord.Embed(
                colour=discord.Colour.from_rgb(66, 135, 245),
                title=f"Profile of {icname}",
                timestamp=ctx.message.created_at
                )
                embed.add_field(name='ID:', value=f'{icid}', inline=False)
                embed.add_field(name=f'Followers:', value=f'{icfollowers}', inline=False)
                embed.add_field(name='Last login:', value=f'{datetime.datetime.fromtimestamp(round(iclastlogin/1000.0))}', inline=False)
                embed.add_field(name='Amount of maps:', value=f'{icmaps}', inline=False)
                embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)

                await ctx.send(embed=embed)
                i = i + 1
            else:
                i = i + 1

@client.command()
async def list(ctx, mode):
    if mode.lower() == "tc":
        x = '2'
    elif mode.lower() == "sim":
        x = '1'
    elif mode.lower() == "misc":
        x = '3'
    else:
        await ctx.send(':warning: Please enter a valid mode!')
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
    if mode.lower() == "tc":
        x = '2'
    elif mode.lower() == "sim":
        x = '1'
    elif mode.lower() == "misc":
        x = '3'
    else:
        await ctx.send(':warning: Please enter a valid mode!')
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

'''
@client.command()
async def suggest(ctx, *, suggestion):
    embed = discord.Embed(
        colour=discord.Colour.from_rgb(66, 135, 245),
        timestamp=ctx.message.created_at,
    )
    embed.add_field(name="Submitter", value=ctx.author.display_name, inline=False)
    embed.add_field(name="Suggestion", value=suggestion, inline=False)
    embed.set_thumbnail(url=ctx.author.avatar_url)

    channel = ctx.bot.get_channel(744653826799435809)#600465489508171776
    #like = ctx.bot.get_emoji(759059895424909380)
    #dislike = ctx.bot.get_emoji(759060520455766036)
    await ctx.message.add_reaction('📬')
    likes = await channel.send(embed=embed)
    #await likes.add_reaction(like)
    #await likes.add_reaction(dislike)
    await likes.add_reaction('🤍')

    dm = discord.Embed(
        colour=discord.Colour.from_rgb(66, 135, 245),
        title='Suggestion has been sent!'
    )
    dm.add_field(name=" ", value=f'Hey {ctx.author.mention}, your suggestion has been sent to the <#600465489508171776> channel so that people can like/dislike it!', inline=False)
    dm.add_field(name=" ", value='Please wait until someone votes for it.', inline=False)
    dm.add_field(name="Your suggestion was:", value=f'`{suggestion}`', inline=False)
    dm.set_footer(text=f'Replied to a suggestion by: {ctx.message.author}', icon_url=ctx.author.avatar_url)

    await ctx.author.send(embed=dm)'''

@client.command()
async def help(ctx):
    embed = discord.Embed(
        colour=discord.Colour.from_rgb(66, 135, 245),
        title=f'Need some help?',
        timestamp=ctx.message.created_at
    )
    embed.add_field(name='Help', value='Shows this command', inline=False)
    embed.add_field(name='Userinfo', value='Gets user info from a mention! required arguments: `ic userinfo <@mention>` (requires a linked account)', inline=False)
    embed.add_field(name='Link', value='Links a IC account to a Discord account (admin only)', inline=False)
    embed.add_field(name='Unlink', value='Unlinks a IC account from a Discord account (admin only)', inline=False)
    embed.add_field(name='Search', value='Searches for users', inline=False)
    embed.add_field(name='Profile', value='Checks a profile of a user', inline=False)
    embed.add_field(name='Trending', value="Shows the map which is currenly first in the trending category! required arguments: `ic trending <sim>/<tc>/<misc>`", inline=False)
    embed.add_field(name='List', value="Shows a list of top 12 maps from the trending category! required arguments: `ic list <sim>/<tc>/<misc>`")
    embed.add_field(name='Suggest', value='Suggest a new feature to the Dev! it will be posted in <#600465489508171776>', inline=False)
    embed.add_field(name='Verify', value='Verify a new user! required arguments: `ic verify <@mention> <id>` (admin-only)', inline=False)
    embed.add_field(name='Ping', value="Checks the client's latency", inline=False)
    embed.add_field(name='Cheats', value='Shows all the cheats', inline=False)
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
        title="Cheats",
        description='**Here are the current "cheats" which will not break the game:**\n\n\n**Fps** - Displays an FPS counter.\n\n**RegnarDet?** - Forces the weather to rain.\n\n**TorsVrede** - Forces the weather to thunderstorm.\n\n**Solkatt** - Forces the weather to sunny.\n\n**Dimfilt** - Forces the weather to fog.\n\n**Väderlek or Vaderlek** - Sets the weather to the default dynamic setting.\n\n**Händelser or Handelser** - Random events are triggered as often as possible.\n\n**Ögonsten or Ogonsten** - Graphics settings not lowered when zooming out.\n\n**GömdaSaker or GomdaSaker** - Unlocks all decorative objects.\n\n**Uppdatera** - Opens the update link for your installation (shadowtree.se / Google Play / Amazon)\n\n**Blindstyre** - Disables vehicles stopping before crashed vehicles.',
        timestamp=ctx.message.created_at
    )
    embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

client.run(token.read())