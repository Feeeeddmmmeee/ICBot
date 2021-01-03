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

    @commands.command(aliases=['sendoutside'])
    @commands.has_permissions(manage_roles=True)
    async def outsider(self, ctx, member : discord.Member):
        outsider = discord.utils.get(ctx.guild.roles,name='outsider :(')
        unverified = discord.utils.get(ctx.guild.roles,name="Unverified")

        await member.add_roles(outsider)

        await member.remove_roles(unverified)

        embed = discord.Embed(
            colour=discord.Colour.from_rgb(66, 135, 245),
            description=f'**An administrator has successfully verified** {member.mention}**!**',
            timestamp=ctx.message.created_at
        )
        embed.set_footer(text=f'Verified by {ctx.author}', icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def bypass(self, ctx, member : discord.Member):
        player = discord.utils.get(ctx.guild.roles,name="IC player")
        unverified = discord.utils.get(ctx.guild.roles,name="Unverified")

        await member.add_roles(player)

        await member.remove_roles(unverified)

        embed = discord.Embed(
            colour=discord.Colour.from_rgb(66, 135, 245),
            description=f'**An administrator has successfully bypassed** {member.mention}**!**',
            timestamp=ctx.message.created_at
        )
        embed.set_footer(text=f'Bypassed by {ctx.author}', icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def verify(self, ctx, member : discord.Member, id):
        channel = ctx.bot.get_channel(469863046408306699)
        async with ctx.typing():
            answer = requests.get(f"https://tl3.shadowtree-software.se/TL3BackEnd/rest/user2/public/info/{id}", verify = False)
        api = answer.json()
        icname = api['name']

        with open('accounts.json', 'r') as f:
            accounts = json.load(f)

        accounts[str(member.id)] = id

        with open('accounts.json', 'w') as f:
            json.dump(accounts, f, indent=4)

        sort()

        player = discord.utils.get(ctx.guild.roles,name="IC player")
        unverified = discord.utils.get(ctx.guild.roles,name="Unverified")

        await member.add_roles(player)

        await member.remove_roles(unverified)

        embed = discord.Embed(
            colour=discord.Colour.from_rgb(66, 135, 245),
            description=f'**An administrator has successfully verified** {member.mention}**!**',
            timestamp=ctx.message.created_at
        )
        embed.set_footer(text=f'Verified by {ctx.author}', icon_url=ctx.author.avatar_url)

        await ctx.channel.purge(limit=1)
        await member.edit(nick=icname)

        await ctx.send(embed=embed)

        welcome = discord.Embed(
            colour=discord.Colour.from_rgb(66, 135, 245),
            description="A new user has been verified!"
        )
        welcome.set_author(name=member, icon_url=member.avatar_url)

        await channel.send(embed=welcome)

        dm = discord.Embed(
            colour=discord.Colour.from_rgb(66, 135, 245),
            title='You have been verified!'
        )
        dm.add_field(name="Hey! :wave:", value=f'Hey {member.mention}, You have been successfully verified by a staff member!', inline=False)
        dm.add_field(name="But.. what does that mean?", value='We have linked your IC account to your discord and now people can run the `ic userinfo <mention>` command to view your profile!', inline=False)
        dm.set_footer(text=f'You were verified by: {ctx.author}', icon_url=ctx.author.avatar_url)
        await member.send(embed=dm)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def link(self, ctx, member : discord.Member, id):
        with open('accounts.json', 'r') as f:
            accounts = json.load(f)

        accounts[str(member.id)] = id

        with open('accounts.json', 'w') as f:
            json.dump(accounts, f, indent=4)
        
        await ctx.send(f"Successfully linked an account to {member.mention}!")

        sort()

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unlink(self, ctx, member : discord.Member):
        with open('accounts.json', 'r') as f:
            accounts = json.load(f)

        accounts.pop(str(member.id))

        with open('accounts.json', 'w') as f:
            json.dump(accounts, f, indent=4)

        await ctx.send(f"Successfully unlinked an account from {member.mention}!")

    @commands.command(aliases = ['info', 'user', 'ui'])
    async def userinfo(self, ctx, member : discord.Member=None):
        member = ctx.author if not member else member
        id = member.id
        with open('accounts.json', 'r') as f:
            accounts = json.load(f)

        if str(member.id) in accounts:
            icId = accounts[str(id)]

            async with ctx.typing():
                response = requests.get(f"https://tl3.shadowtree-software.se/TL3BackEnd/rest/user2/public/info/{icId}", verify = False)
            api = response.json()
            icname = api['name']
            icfollowers = api['followers']
            iclastlogin = api['lastLogin']
            icmaps = api['maps']
            icid = api['objectId']

            embed = discord.Embed(
            colour=discord.Colour.from_rgb(66, 135, 245),
            timestamp=ctx.message.created_at
            )
            embed.set_author(name=member, icon_url=member.avatar_url)
            embed.add_field(name='Intersection Controller', value=f'Nickname: {icname}\nID: {icid}\nFollowers: {icfollowers}\nLast login: {datetime.datetime.fromtimestamp(round(iclastlogin/1000.0))}\nAmount of maps: {icmaps}', inline=False)
            embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)

            await ctx.send(embed=embed)
        else:
            await ctx.send(f":warning: Seems like {member.mention}'s account is not linked to his discord! If you'd like to link it please contact the administrators.")


def setup(client):
    client.add_cog(Commands(client))