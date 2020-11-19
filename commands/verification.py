import discord
import datetime
import random
import json
import os
import asyncio
import requests
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, MissingPermissions

class Commands(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    @commands.command()
    @has_permissions(administrator=True)
    async def verify(self, ctx, member : discord.Member, id):
        guild = ctx.guild
        answer = requests.get(f"https://tl3.shadowtree-software.se/TL3BackEnd/rest/user2/public/info/{id}", verify = False)
        api = answer.json()
        icname = api['name']


        with open('accounts.json', 'r') as f:
            accounts = json.load(f)

        accounts[str(member.id)] = id

        with open('accounts.json', 'w') as f:
            json.dump(accounts, f, indent=4)

        for role in guild.roles:
            if role.name == 'IC player':
                await member.add_roles(role)

        for role in guild.roles:
            if role.name == 'Unverified':
                await member.remove_roles(role)

        embed = discord.Embed(
            colour=discord.Colour.from_rgb(66, 135, 245),
            description=f'**An administrator has successfully verified** {member.mention}**!**',
            timestamp=ctx.message.created_at
        )
        embed.set_footer(text=f'Verified by {ctx.author}', icon_url=ctx.author.avatar_url)

        await ctx.channel.purge(limit=1)
        await member.edit(nick=icname)

        await ctx.send(embed=embed)

    @commands.command()
    @has_permissions(administrator=True)
    async def link(self, ctx, member : discord.Member, id):
        with open('accounts.json', 'r') as f:
            accounts = json.load(f)

        accounts[str(member.id)] = id

        with open('accounts.json', 'w') as f:
            json.dump(accounts, f, indent=4)
        
        await ctx.send(f"Successfully linked an account to {member.mention}!")

    @commands.command()
    @has_permissions(administrator=True)
    async def unlink(self, ctx, member : discord.Member):
        with open('accounts.json', 'r') as f:
            accounts = json.load(f)

        accounts.pop(str(member.id))

        with open('accounts.json', 'w') as f:
            json.dump(accounts, f, indent=4)

        await ctx.send(f"Successfully unlinked an account from {member.mention}!")

    @commands.command(alises = ['info', 'user'])
    async def userinfo(self, ctx, member : discord.Member):
        id = member.id
        print(id)
        with open('accounts.json', 'r') as f:
            accounts = json.load(f)

        icId = accounts[str(id)]

        response = requests.get(f"https://tl3.shadowtree-software.se/TL3BackEnd/rest/user2/public/info/{icId}", verify = False)
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


def setup(client):
    client.add_cog(Commands(client))