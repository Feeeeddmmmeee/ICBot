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
        if number == '1':
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(66, 135, 245),
                title='1. Swearing',
                description='Keep swearing to a minimum, we want a toxic free enviroment!'
            )
        elif number == '2':
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(66, 135, 245),
                title='2. Spamming Content',
                description='Repeatedly sending unnecessary and random messages (5 or more times) in any channel will result in a 10+ minute mute. (except <#597986251659935755>)'
            )
        elif number == '3':
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(66, 135, 245),
                title='3. Argumentative Situations',
                description='Anybody causing argumentative situations or drama can result in Administrative Action being taken against themselves.'
            )
        elif number == '4':
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(66, 135, 245),
                title='4. Disrespectful Actions',
                description='Do not disrespect anyone in this server, this also includes derogatory terms, slurs, racism or other offensive material.'
            )
        elif number == '5':
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(66, 135, 245),
                title='5. Not Safe For Work Content',
                description='NSFW is not allowed, this will result in a temporary ban or permanent ban from the server'
            )
        elif number == '6':
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(66, 135, 245),
                title='6. Self Advertisement',
                description='Do not DM anyone a server invite (without permission). **If you own a guild of people from one country who are all playing IC feel free to ask us to add it to <#769620613580455946>!**'
            )
        elif number == '7':
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(66, 135, 245),
                title='7. Nicknames',
                description="Your server nickname must be identical as your in-game nickname. No trolling with nicks and profile pictures. Admins can change the nick if they don't approve it. No useless changes of your IC nickname are permitted, it may also count as violating rule 7."
            )
        elif number == '8':
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(66, 135, 245),
                title='8. IC Life',
                description='Your IC life will determine if you are trusted. Bullies and hackers get ban.'
            )
        elif number == '9':
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(66, 135, 245),
                title='9. Channel Relevance',
                description='Keep relevant topics in their correct text channels.'
            )
        elif number == '10':
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(66, 135, 245),
                title='10. Appropriate Profile Pictures',
                description='Have appropriate profile pictures, they may not be pornography, or have relations to a terrorist organization or a cult. Absolutely no trolling with profile pictures.'
            )
        elif number == '11':
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(66, 135, 245),
                title='11. Harassment',
                description='Harassing other people will result in a mute or a kick from the server.'
            )
        elif number == '12':
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(66, 135, 245),
                title='12. Drugs',
                description='You are not allowed to be under the influence of drugs, etc. while chatting.'
            )
        elif number == '13':
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(66, 135, 245),
                title='13. MiniModding ',
                description="MiniModding is prohibited, this includes continuously correcting someone’s actions, asking for someone’s ban, mute or other administrative action taken against another, or asking for demotion of admins. Don't act like you were an admin, because you will get a strict punishment."
            )
        elif number == '14':
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(66, 135, 245),
                title='14. Pinging',
                description="No unnecessary pinging other members is allowed. It's especially prohibited to ping the owner, the admins, and the whole roles. You can get a role to get pinged when there are important news in the server, you get it by typing `?rank Notifications-Server` in <#709323713207599134>."
            )
        elif number == '15':
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(66, 135, 245),
                title='15. Evasion',
                description='Absolutely no trying to make a loophole around the rules, doing such will result in further punishment than already established.'
            )
        elif number == '16':
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(66, 135, 245),
                title='16. Alt accounts ',
                description="You are only allowed to join with your alt account, if you state that it's you. Hiding your alt will result in kicking it."
            )
        elif number == '17':
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(66, 135, 245),
                title='17. Personal information',
                description='Without permission of the person, you are not allowed to reveal and share their personal information, such as name, adress, age, etc. This goes also for leaking DMs (Direct Messages).'
            )
        elif number == '18':
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(66, 135, 245),
                title='18. Admins',
                description='Admins also have to follow the server rules. They punish people only depending on the severity of the issue. Admins are always right in arguments about rules and punishments.'
            )
        
            
            
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Commands(client))
