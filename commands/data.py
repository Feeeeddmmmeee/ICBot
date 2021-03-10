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
    async def data(self, ctx, arg1, arg2, arg3, arg4 = None, arg5 = None, arg6 = None, arg7 = None):
        cross = self.client.get_emoji(798573872916070470)
        tick = self.client.get_emoji(798573863184236574)
        if arg1 == "get":
            if arg2 == "user":
                if arg3 == "from":
                    if arg4 == "name":
                        response = requests.get(f"https://tl3.shadowtree-software.se/TL3BackEnd/rest/user2/public/search?query={arg5.replace(' ', '%20')}", verify = False)
                        api = response.json()
                        if len(api):
                            for item in api:
                                if item["name"] == arg5:
                                    response = requests.get(f"https://tl3.shadowtree-software.se/TL3BackEnd/rest/user2/public/info/{item['objectId']}", verify = False)
                                    break
                            api = response.json()
                            if arg6 == None:
                                embed = discord.Embed(title = f"{tick} Here's the result:", description = f"name: {api['name']},\nfollowers: {api['followers']},\nmaps: {api['maps']},\nlastLogin: {api['lastLogin']},\nobjectId: {api['objectId']}", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                                embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                                await ctx.send(embed = embed)
                            elif arg6 == "name":
                                embed = discord.Embed(title = f"{tick} Here's the result:", description = f"name: {api['name']}", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                                embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                                await ctx.send(embed = embed)
                            elif arg6 == "followers":
                                embed = discord.Embed(title = f"{tick} Here's the result:", description = f"followers: {api['followers']}", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                                embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                                await ctx.send(embed = embed)
                            elif arg6 == "maps":
                                embed = discord.Embed(title = f"{tick} Here's the result:", description = f"maps: {api['maps']}", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                                embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                                await ctx.send(embed = embed)
                            elif arg6 == "lastlogin":
                                embed = discord.Embed(title = f"{tick} Here's the result:", description = f"lastLogin: {api['lastLogin']}", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                                embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                                await ctx.send(embed = embed)
                            elif arg6 == "objectid":
                                embed = discord.Embed(title = f"{tick} Here's the result:", description = f"objectId: {api['objectId']}", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                                embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                                await ctx.send(embed = embed)
                            elif arg6 == "raw":
                                embed = discord.Embed(title = f"{tick} Here's the result:", description = f"```json\n{str(api)}```", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                                embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                                await ctx.send(embed = embed)
                            else:
                                await ctx.send(f"{cross} Invalid argument!")
                        else: 
                            await ctx.send(f"{cross} Invalid user id!")
                    elif arg4 == "discord":
                        with open("accounts.json", "r") as f:
                            accounts = json.load(f)
                        response = requests.get(f"https://tl3.shadowtree-software.se/TL3BackEnd/rest/user2/public/info/{accounts[arg5].replace(' ', '%20')}", verify = False)
                        api = response.json()
                        if len(api):
                            if arg6 == None:
                                embed = discord.Embed(title = f"{tick} Here's the result:", description = f"name: {api['name']},\nfollowers: {api['followers']},\nmaps: {api['maps']},\nlastLogin: {api['lastLogin']},\nobjectId: {api['objectId']}", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                                embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                                await ctx.send(embed = embed)
                            elif arg6 == "name":
                                embed = discord.Embed(title = f"{tick} Here's the result:", description = f"name: {api['name']}", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                                embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                                await ctx.send(embed = embed)
                            elif arg6 == "followers":
                                embed = discord.Embed(title = f"{tick} Here's the result:", description = f"followers: {api['followers']}", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                                embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                                await ctx.send(embed = embed)
                            elif arg6 == "maps":
                                embed = discord.Embed(title = f"{tick} Here's the result:", description = f"maps: {api['maps']}", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                                embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                                await ctx.send(embed = embed)
                            elif arg6 == "lastlogin":
                                embed = discord.Embed(title = f"{tick} Here's the result:", description = f"lastLogin: {api['lastLogin']}", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                                embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                                await ctx.send(embed = embed)
                            elif arg6 == "objectid":
                                embed = discord.Embed(title = f"{tick} Here's the result:", description = f"objectId: {api['objectId']}", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                                embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                                await ctx.send(embed = embed)
                            elif arg6 == "raw":
                                embed = discord.Embed(title = f"{tick} Here's the result:", description = f"```json\n{str(api)}```", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                                embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                                await ctx.send(embed = embed)
                            else:
                                await ctx.send(f"{cross} Invalid argument!")
                        else: 
                            await ctx.send(f"{cross} Invalid user id!")
                    elif arg4 == "api":
                        if "https://tl3.shadowtree-software.se/TL3BackEnd/rest/" in arg5:
                            if "/info" in arg5 or "/search" in arg5:
                                response = requests.get(arg5, verify = False)
                                api = response.json()
                                response = requests.get(f"https://tl3.shadowtree-software.se/TL3BackEnd/rest/user2/public/info/{api['objectId']}", verify = False)
                                api = response.json()
                                if len(api):
                                    if arg6 == None:
                                        embed = discord.Embed(title = f"{tick} Here's the result:", description = f"name: {api['name']},\nfollowers: {api['followers']},\nmaps: {api['maps']},\nlastLogin: {api['lastLogin']},\nobjectId: {api['objectId']}", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                                        embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                                        await ctx.send(embed = embed)
                                    elif arg6 == "name":
                                        embed = discord.Embed(title = f"{tick} Here's the result:", description = f"name: {api['name']}", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                                        embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                                        await ctx.send(embed = embed)
                                    elif arg6 == "followers":
                                        embed = discord.Embed(title = f"{tick} Here's the result:", description = f"followers: {api['followers']}", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                                        embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                                        await ctx.send(embed = embed)
                                    elif arg6 == "maps":
                                        embed = discord.Embed(title = f"{tick} Here's the result:", description = f"maps: {api['maps']}", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                                        embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                                        await ctx.send(embed = embed)
                                    elif arg6 == "lastlogin":
                                        embed = discord.Embed(title = f"{tick} Here's the result:", description = f"lastLogin: {api['lastLogin']}", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                                        embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                                        await ctx.send(embed = embed)
                                    elif arg6 == "objectid":
                                        embed = discord.Embed(title = f"{tick} Here's the result:", description = f"objectId: {api['objectId']}", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                                        embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                                        await ctx.send(embed = embed)
                                    elif arg6 == "raw":
                                        embed = discord.Embed(title = f"{tick} Here's the result:", description = f"```json\n{str(api)}```", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                                        embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                                        await ctx.send(embed = embed)
                                    else:
                                        await ctx.send(f"{cross} Invalid argument!")
                            elif "/user" in arg5:
                                response = requests.get(arg5, verify = False)
                                api = response.json()
                                response = requests.get(f"https://tl3.shadowtree-software.se/TL3BackEnd/rest/user2/public/info/{api[0]['author']}", verify = False)
                                api = response.json()
                                if len(api):
                                    if arg6 == None:
                                        embed = discord.Embed(title = f"{tick} Here's the result:", description = f"name: {api['name']},\nfollowers: {api['followers']},\nmaps: {api['maps']},\nlastLogin: {api['lastLogin']},\nobjectId: {api['objectId']}", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                                        embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                                        await ctx.send(embed = embed)
                                    elif arg6 == "name":
                                        embed = discord.Embed(title = f"{tick} Here's the result:", description = f"name: {api['name']}", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                                        embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                                        await ctx.send(embed = embed)
                                    elif arg6 == "followers":
                                        embed = discord.Embed(title = f"{tick} Here's the result:", description = f"followers: {api['followers']}", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                                        embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                                        await ctx.send(embed = embed)
                                    elif arg6 == "maps":
                                        embed = discord.Embed(title = f"{tick} Here's the result:", description = f"maps: {api['maps']}", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                                        embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                                        await ctx.send(embed = embed)
                                    elif arg6 == "lastlogin":
                                        embed = discord.Embed(title = f"{tick} Here's the result:", description = f"lastLogin: {api['lastLogin']}", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                                        embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                                        await ctx.send(embed = embed)
                                    elif arg6 == "objectid":
                                        embed = discord.Embed(title = f"{tick} Here's the result:", description = f"objectId: {api['objectId']}", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                                        embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                                        await ctx.send(embed = embed)
                                    elif arg6 == "raw":
                                        embed = discord.Embed(title = f"{tick} Here's the result:", description = f"```json\n{str(api)}```", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                                        embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                                        await ctx.send(embed = embed)
                                    else:
                                        await ctx.send(f"{cross} Invalid argument!")
                            else:
                                await ctx.send(f"{cross} Please pass in a supported api link!")
                        else:
                            await ctx.send(f"{cross} Please pass in a supported api link!")
                else:
                    response = requests.get(f"https://tl3.shadowtree-software.se/TL3BackEnd/rest/user2/public/info/{arg3}", verify = False)
                    api = response.json()
                    if len(api):
                        if arg4 == None:
                            embed = discord.Embed(title = f"{tick} Here's the result:", description = f"name: {api['name']},\nfollowers: {api['followers']},\nmaps: {api['maps']},\nlastLogin: {api['lastLogin']},\nobjectId: {api['objectId']}", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                            embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                            await ctx.send(embed = embed)
                        elif arg4 == "name":
                            embed = discord.Embed(title = f"{tick} Here's the result:", description = f"name: {api['name']}", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                            embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                            await ctx.send(embed = embed)
                        elif arg4 == "followers":
                            embed = discord.Embed(title = f"{tick} Here's the result:", description = f"followers: {api['followers']}", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                            embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                            await ctx.send(embed = embed)
                        elif arg4 == "maps":
                            embed = discord.Embed(title = f"{tick} Here's the result:", description = f"maps: {api['maps']}", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                            embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                            await ctx.send(embed = embed)
                        elif arg4 == "lastlogin":
                            embed = discord.Embed(title = f"{tick} Here's the result:", description = f"lastLogin: {api['lastLogin']}", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                            embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                            await ctx.send(embed = embed)
                        elif arg4 == "objectid":
                            embed = discord.Embed(title = f"{tick} Here's the result:", description = f"objectId: {api['objectId']}", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                            embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                            await ctx.send(embed = embed)
                        elif arg4 == "raw":
                            embed = discord.Embed(title = f"{tick} Here's the result:", description = f"```json\n{str(api)}```", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                            embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                            await ctx.send(embed = embed)
                        else:
                            await ctx.send(f"{cross} Invalid argument!")
                    else: 
                        await ctx.send(f"{cross} Invalid user id!")
            elif arg2 == "map":
                if arg3 == "user":
                    if arg4 == "id":
                        if arg6 == None:
                            response = requests.get(f"https://tl3.shadowtree-software.se/TL3BackEnd/rest/map/public/user/{arg5}?result=1&page=0", verify = False)
                            api = response.json()
                            embed = discord.Embed(title = f"{tick} Here's the result:", description = f"name: {api[0]['name']}\ndesc: {api[0]['desc']}\ngameModeGroup: {api[0]['gameModeGroup']}\nauthorName: {api[0]['authorName']}\nauthor: {api[0]['author']}", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                            embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                            await ctx.send(embed = embed)
                        else:
                            if arg7 == "raw":
                                response = requests.get(f"https://tl3.shadowtree-software.se/TL3BackEnd/rest/map/public/user/{arg5}?result=1&page={arg6}", verify = False)
                                api = response.json()
                                embed = discord.Embed(title = f"{tick} Here's the result:", description = f"```json\n{str(api)}```", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                                embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                                await ctx.send(embed = embed)
                            else:
                                response = requests.get(f"https://tl3.shadowtree-software.se/TL3BackEnd/rest/map/public/user/{arg5}?result=1&page={arg6}", verify = False)
                                api = response.json()
                                embed = discord.Embed(title = f"{tick} Here's the result:", description = f"name: {api[0]['name']}\ndesc: {api[0]['desc']}\ngameModeGroup: {api[0]['gameModeGroup']}\nauthorName: {api[0]['authorName']}\nauthor: {api[0]['author']}", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                                embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                                await ctx.send(embed = embed)
                    elif arg4 == "name":
                        response = requests.get(f"https://tl3.shadowtree-software.se/TL3BackEnd/rest/user2/public/search?query={arg5.replace(' ', '%20')}", verify = False)
                        api = response.json()
                        if len(api):
                            for item in api:
                                if item["name"] == arg5:
                                    if arg6 == None:
                                        response = requests.get(f"https://tl3.shadowtree-software.se/TL3BackEnd/rest/map/public/user/{item['objectId']}?result=1&page=0", verify = False)
                                        api = response.json()
                                        embed = discord.Embed(title = f"{tick} Here's the result:", description = f"name: {api[0]['name']}\ndesc: {api[0]['desc']}\ngameModeGroup: {api[0]['gameModeGroup']}\nauthorName: {api[0]['authorName']}\nauthor: {api[0]['author']}", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                                        embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                                        await ctx.send(embed = embed)
                                    else:
                                        if arg7 == "raw":
                                            response = requests.get(f"https://tl3.shadowtree-software.se/TL3BackEnd/rest/map/public/user/{item['objectId']}?result=1&page={arg6}", verify = False)
                                            api = response.json()
                                            embed = discord.Embed(title = f"{tick} Here's the result:", description = f"```json\n{str(api)}```", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                                            embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                                            await ctx.send(embed = embed)
                                        else:
                                            response = requests.get(f"https://tl3.shadowtree-software.se/TL3BackEnd/rest/map/public/user/{item['objectId']}?result=1&page={arg6}", verify = False)
                                            api = response.json()
                                            embed = discord.Embed(title = f"{tick} Here's the result:", description = f"name: {api[0]['name']}\ndesc: {api[0]['desc']}\ngameModeGroup: {api[0]['gameModeGroup']}\nauthorName: {api[0]['authorName']}\nauthor: {api[0]['author']}", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                                            embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                                            await ctx.send(embed = embed)
                                    break
                elif arg3 == "discord":
                    with open("accounts.json", "r") as f:
                        accounts = json.load(f)
                    if arg5 == None:
                        response = requests.get(f"https://tl3.shadowtree-software.se/TL3BackEnd/rest/map/public/user/{accounts[arg4]}?result=1&page=0", verify = False)
                        api = response.json()
                        embed = discord.Embed(title = f"{tick} Here's the result:", description = f"name: {api[0]['name']}\ndesc: {api[0]['desc']}\ngameModeGroup: {api[0]['gameModeGroup']}\nauthorName: {api[0]['authorName']}\nauthor: {api[0]['author']}", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                        embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                        await ctx.send(embed = embed)
                    else:
                        if arg6 == "raw":
                            response = requests.get(f"https://tl3.shadowtree-software.se/TL3BackEnd/rest/map/public/user/{arg4}?result=1&page={arg5}", verify = False)
                            api = response.json()
                            embed = discord.Embed(title = f"{tick} Here's the result:", description = f"```json\n{str(api)}```", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                            embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                            await ctx.send(embed = embed)
                        else:
                            response = requests.get(f"https://tl3.shadowtree-software.se/TL3BackEnd/rest/map/public/user/{accounts[arg4]}?result=1&page={arg5}", verify = False)
                            api = response.json()
                            embed = discord.Embed(title = f"{tick} Here's the result:", description = f"name: {api[0]['name']}\ndesc: {api[0]['desc']}\ngameModeGroup: {api[0]['gameModeGroup']}\nauthorName: {api[0]['authorName']}\nauthor: {api[0]['author']}", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                            embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                            await ctx.send(embed = embed)
                elif arg3 == "api":
                    if "https://tl3.shadowtree-software.se/TL3BackEnd/rest/" in arg4:
                        if "/info" in arg4 or "/search" in arg4:
                            response = requests.get(arg4, verify = False)
                            api = response.json()
                            response = requests.get(f"https://tl3.shadowtree-software.se/TL3BackEnd/rest/user2/public/info/{api['objectId']}", verify = False)
                            api = response.json()
                            if len(api):
                                if arg5 == None:
                                    response = requests.get(f"https://tl3.shadowtree-software.se/TL3BackEnd/rest/map/public/user/{api['objectId']}?result=1&page=0", verify = False)
                                    api = response.json()
                                    embed = discord.Embed(title = f"{tick} Here's the result:", description = f"name: {api[0]['name']}\ndesc: {api[0]['desc']}\ngameModeGroup: {api[0]['gameModeGroup']}\nauthorName: {api[0]['authorName']}\nauthor: {api[0]['author']}", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                                    embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                                    await ctx.send(embed = embed)
                                else:
                                    if arg6 == "raw":
                                        response = requests.get(f"https://tl3.shadowtree-software.se/TL3BackEnd/rest/map/public/user/{api['objectId']}?result=1&page={arg5}", verify = False)
                                        api = response.json()
                                        embed = discord.Embed(title = f"{tick} Here's the result:", description = f"```json\n{str(api)}```", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                                        embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                                        await ctx.send(embed = embed)
                                    else:
                                        response = requests.get(f"https://tl3.shadowtree-software.se/TL3BackEnd/rest/map/public/user{api['objectId']}?result=1&page={arg5}", verify = False)
                                        api = response.json()
                                        embed = discord.Embed(title = f"{tick} Here's the result:", description = f"name: {api[0]['name']}\ndesc: {api[0]['desc']}\ngameModeGroup: {api[0]['gameModeGroup']}\nauthorName: {api[0]['authorName']}\nauthor: {api[0]['author']}", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                                        embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                                        await ctx.send(embed = embed)
                        elif "/user" in arg4:
                            response = requests.get(arg4, verify = False)
                            api = response.json()
                            response = requests.get(f"https://tl3.shadowtree-software.se/TL3BackEnd/rest/user2/public/info/{api[0]['author']}", verify = False)
                            api = response.json()
                            if len(api):
                                if arg5 == None:
                                    response = requests.get(f"https://tl3.shadowtree-software.se/TL3BackEnd/rest/map/public/user/{api['objectId']}?result=1&page=0", verify = False)
                                    api = response.json()
                                    embed = discord.Embed(title = f"{tick} Here's the result:", description = f"name: {api[0]['name']}\ndesc: {api[0]['desc']}\ngameModeGroup: {api[0]['gameModeGroup']}\nauthorName: {api[0]['authorName']}\nauthor: {api[0]['author']}", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                                    embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                                    await ctx.send(embed = embed)
                                else:
                                    if arg6 == "raw":
                                        response = requests.get(f"https://tl3.shadowtree-software.se/TL3BackEnd/rest/map/public/user/{api['objectId']}?result=1&page={arg5}", verify = False)
                                        api = response.json()
                                        embed = discord.Embed(title = f"{tick} Here's the result:", description = f"```json\n{str(api)}```", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                                        embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                                        await ctx.send(embed = embed)
                                    elif arg6 == None:
                                        response = requests.get(f"https://tl3.shadowtree-software.se/TL3BackEnd/rest/map/public/user/{api['objectId']}?result=1&page={arg5}", verify = False)
                                        api = response.json()
                                        embed = discord.Embed(title = f"{tick} Here's the result:", description = f"name: {api[0]['name']}\ndesc: {api[0]['desc']}\ngameModeGroup: {api[0]['gameModeGroup']}\nauthorName: {api[0]['authorName']}\nauthor: {api[0]['author']}", colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                                        embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                                        await ctx.send(embed = embed)
                        else:
                            await ctx.send(f"{cross} Please pass in a supported api link!")
                    else:
                        await ctx.send(f"{cross} Please pass in a supported api link!")
            else:
                await ctx.send(f"{cross} Invalid argument!")
        elif arg1 == "modify":
            if ctx.author.id == 585115156757872653:
                await ctx.send("not done yet")
            else:
                await ctx.send(f"{cross} Only the bot owner can run this command!")
        else:
            await ctx.send(f"{cross} The first argument can only be set to get/modify!")

def setup(client):
    client.add_cog(Commands(client))