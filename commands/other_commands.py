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

    @commands.command(aliases = ['map'])
    async def maps(self, ctx, id, number):
        cross = self.client.get_emoji(798573872916070470)
        dislike = self.client.get_emoji(759060520455766036)
        like = self.client.get_emoji(759059895424909380)
        async with ctx.typing():
            response = requests.get(f"https://tl3.shadowtree-software.se/TL3BackEnd/rest/map/public/user/{id}?result=1&page={number}", verify = False)
        api = response.json()
        
        if not(len(api)):
            await ctx.send(f"{cross} This map does not exist!")
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

            if str(int(number)+1).endswith("11"):
                end = "th"

            if api[0]['gameModeGroup'] == 1:
                gamemode = "Simulation"
            elif api[0]['gameModeGroup'] == 2:
                gamemode = "Traffic Controller"
            elif api[0]['gameModeGroup'] == 3:
                gamemode = "Miscellaneous"

            embed = discord.Embed(
                colour=discord.Colour.from_rgb(66, 135, 245),
                title = f"{api[0]['authorName']}'s {str(int(number)+1)}{end} map:",
                timestamp = ctx.message.created_at
            )
            embed.add_field(name=api[0]['name'], value=f'Description: {api[0]["desc"]}\n\nGame Mode: {gamemode}\nAuthor Name: {api[0]["authorName"]}\n{like} Likes: {api[0]["votesUp"]}\n{dislike} Dislikes: {api[0]["votesDown"]}\n🤍 Favorites: {api[0]["favorites"]}')
            embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)

            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_guild_permissions(manage_roles=True)
    async def log(self, ctx, user : discord.User, pType, reason = "Unspecified", duration = "Unspecified", additionalInfo = None):
        with open("config.json", "r") as f:
            config = json.load(f)

        cross = self.client.get_emoji(798573872916070470)
        
        if ctx.guild.id in config["validIds"]:

            logs = ctx.guild.get_channel(ctx.channel.id)#630091908814864404
            with open("config.json", "r") as f:
                config = json.load(f)

            case = config['case'];

            embed = discord.Embed(
                colour = discord.Colour.from_rgb(230, 41, 41)
            )
            embed.set_author(name=f"CASE {(str(case))} [{pType.upper()}] {user.name}#{user.discriminator}", icon_url=user.avatar_url)
            embed.add_field(name="Reason", value=reason)
            if "warn" not in pType.lower() and "kick" not in pType.lower():
                embed.add_field(name="Duration", value=duration)
            if additionalInfo != None:
                embed.add_field(name="Additional Information", value=additionalInfo)

            if len(ctx.message.attachments):
                attachment = ctx.message.attachments[0]
                embed.set_image(url = attachment.url)

            if "warn" in pType.lower():
                embed.colour = discord.Colour.from_rgb(237, 110, 47)
            if "mute" in pType.lower():
                embed.colour = discord.Colour.from_rgb(237, 69, 47)

            await ctx.send(embed=embed)

            case = case + 1
            config['case'] = case

            with open("config.json", "w") as f: json.dump(config, f, indent=4)
        
        else:
            await ctx.send(f"{cross} This commands isn't available in your server!")

def setup(client):
    client.add_cog(Commands(client))