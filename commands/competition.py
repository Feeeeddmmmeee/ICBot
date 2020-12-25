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
    async def host(self, ctx, desc, time):
        with open('competitions.json', 'r') as f:
            competitions = json.load(f)

        

        with open('competitions.json', 'w') as f:
            json.dump(competitions, f, indent=4)
    
def setup(client):
    client.add_cog(Commands(client))