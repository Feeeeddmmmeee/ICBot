import discord
import datetime
import random
import json
import os
import asyncio
import requests
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, MissingPermissions

def sort():
    with open('accounts.json', 'r') as f:
        accounts = json.load(f)

    sortedAccounts = sorted(accounts.items(), key=lambda k: requests.get(f"https://tl3.shadowtree-software.se/TL3BackEnd/rest/user2/public/info/{k[1]}", verify=False).json()["followers"], reverse=True)

    #tuple to dict here
    accounts = dict((x, y) for x, y in sortedAccounts)

    with open('accounts.json', 'w') as f:
        json.dump(accounts, f, indent=4)

class Commands(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def rank(self, ctx, member : discord.Member = None):
        cross = self.client.get_emoji(798573872916070470)
        member = ctx.author if not member else member
        id = member.id
        with open('accounts.json', 'r') as f:
            accounts = json.load(f)

        if str(member.id) in accounts:
            icId = accounts[str(id)]
            async with ctx.typing():
                response = requests.get(f"https://tl3.shadowtree-software.se/TL3BackEnd/rest/user2/public/info/{icId}", verify = False)
            api = response.json()
            followers = api['followers']
            avatar = member.avatar_url

            if followers < 5:
                nextlevelxp = 5
                previouslevelxp = 0
                level = 1
            elif followers < 10:
                nextlevelxp = 10
                previouslevelxp = 5
                level = 2
            elif followers < 15:
                nextlevelxp = 15
                previouslevelxp = 10
                level = 3
            elif followers < 25:
                nextlevelxp = 25
                previouslevelxp = 15
                level = 4
            elif followers < 50:
                nextlevelxp = 50
                previouslevelxp = 25
                level = 5
            elif followers < 100:
                nextlevelxp = 100
                previouslevelxp = 50
                level = 6
            elif followers < 150:
                nextlevelxp = 150
                previouslevelxp = 100
                level = 7
            elif followers < 200:
                nextlevelxp = 200
                previouslevelxp = 150
                level = 8
            elif followers < 300:
                nextlevelxp = 300
                previouslevelxp = 200
                level = 9
            elif followers < 400:
                nextlevelxp = 400
                previouslevelxp = 300
                level = 10
            elif followers < 500:
                nextlevelxp = 500
                previouslevelxp = 400
                level = 11
            elif followers < 600:
                nextlevelxp = 600
                previouslevelxp = 500
                level = 12
            elif followers < 750:
                nextlevelxp = 750
                previouslevelxp = 600
                level = 13
            elif followers < 1000:
                nextlevelxp = 1000
                previouslevelxp = 750
                level = 14
            elif followers < 1250:
                nextlevelxp = 1250
                previouslevelxp = 1000
                level = 15
            elif followers < 1500:
                nextlevelxp = 1500
                previouslevelxp = 1250
                level = 16
            elif followers < 2000:
                nextlevelxp = 2000
                previouslevelxp = 1500
                level = 17
            elif followers < 3000:
                nextlevelxp = 3000
                previouslevelxp = 2000
                level = 18
            elif followers < 5000:
                nextlevelxp = 4000
                previouslevelxp = 3000
                level - 19
            else:
                nextlevelxp = followers
                previouslevelxp = 5000
                level = 20
                

            with open('accounts.json', 'r') as f:
                accounts = json.load(f)

            rank = 1
                
            rank = list(accounts).index(str(id)) + 1

            if discord.utils.find(lambda r: r.id == 638082632697118773, ctx.guild.roles) in member.roles:
                boost = "true"
                xpcolor = "de5bd9"
            else:
                boost = "false"
                xpcolor = "3983c6"

            await ctx.send(f"https://vacefron.nl/api/rankcard?username={member.name.replace(' ', '%20')}&avatar={avatar}&level={level}&rank={rank}&currentxp={followers}&nextlevelxp={nextlevelxp}&previouslevelxp={previouslevelxp}&isboosting={boost}&xpcolor={xpcolor}")

        else:
            await ctx.send(f"{cross} Seems like {member.mention}'s account is not linked to his discord! If you'd like to link it please contact the administrators.")


    @commands.command()
    async def leaderboard(self, ctx):
        with open('accounts.json', 'r') as f:
            accounts = json.load(f)

        embed = discord.Embed(
            colour=discord.Colour.from_rgb(66, 135, 245),
            title = "Top 5 users",
            timestamp=ctx.message.created_at
            )
        embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)

        for i in range(0, 5):
            embed.add_field(name=f"{i+1}. {requests.get(f'https://tl3.shadowtree-software.se/TL3BackEnd/rest/user2/public/info/{accounts[list(accounts)[i]]}', verify=False).json()['name']}", value= self.client.get_user(int(list(accounts)[i])).mention, inline=False)
            
        await ctx.send(embed=embed)

        

def setup(client):
    client.add_cog(Commands(client))