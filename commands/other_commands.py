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
    async def maps(self, ctx, id, number):
        cross = self.client.get_emoji(798573872916070470)
        async with ctx.typing():
            response = requests.get(f"https://tl3.shadowtree-software.se/TL3BackEnd/rest/map/public/user/{id}?result=1&page={number}", verify = False)
        api = response.json()
        
        if not(len(api)):
            await ctx.send(f"{cross} We couldn't find any users with this ID!")
            return

        else:

            if str(int(number)+1).endswith("1"):
                end = "st"
            elif str(int(number)+1).endswith("2"):
                end = "nd"
            elif str(int(number)+1).endswith("3"):
                end = "rd"
            else:
                end = "th"

            if api[0]['gameModeGroup'] == 1:
                gamemode = "Simulation"
            elif api[0]['gameModeGroup'] == 2:
                gamemode = "Traffic Controller"
            elif api[0]['gameModeGroup'] == 3:
                gamemode = "Miscellaneous"

            embed = discord.Embed(
                colour=discord.Colour.from_rgb(66, 135, 245),
                title = f"`{id}`'s {str(int(number)+1)}{end} map:",
                timestamp = ctx.message.created_at
            )
            embed.add_field(name=api[0]['name'], value=f'Description: `{api[0]["desc"]}`\n\nGame Mode: {gamemode}\nAuthor Name: {api[0]["authorName"]}\nLikes: {api[0]["votesUp"]}\nDislikes: {api[0]["votesDown"]}\nFavorites: {api[0]["favorites"]}')
            embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)

            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Commands(client))