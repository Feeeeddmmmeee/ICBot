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

    @commands.command(aliases = ["rule"])
    async def rules(self, ctx, number):
        cross = self.client.get_emoji(798573872916070470)
        with open("config.json", "r") as f:
            config = json.load(f)

        if number in config["rules"]:
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(66, 135, 245),
                title=config["rules"][number]["title"],
                description=config["rules"][number]["desc"]
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{cross} Please enter a valid number!")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def update(self, ctx, number, title, *, desc):
        cross = self.client.get_emoji(798573872916070470)
        tick = self.client.get_emoji(798573863184236574)
        with open("config.json", "r") as f:
            config = json.load(f)

        if number in config["rules"]:
            config["rules"][number]["title"] = title
            config["rules"][number]["desc"] = desc

            with open('config.json', 'w') as f:
                json.dump(config, f, indent=4)

            await ctx.send(f"{tick} Successfully edited the rule {number}!")
        else:
            await ctx.send(f"{cross} Please enter a valid number!")

def setup(client):
    client.add_cog(Commands(client))
