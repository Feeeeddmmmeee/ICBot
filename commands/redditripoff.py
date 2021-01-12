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
    async def respect(self, ctx, member : discord.Member):
        cross = self.client.get_emoji(798573872916070470)
        with open("karma.json","r") as f:
            members = json.load(f)

        authorKarma = members[str(ctx.author.id)]

        if member.id != ctx.author.id:
            if authorKarma >= 10:
                if str(member.id) in members:
                    members[str(member.id)] = members[str(member.id)] + 1
                else:
                    members[str(member.id)] = 1

                embed = discord.Embed(colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                embed.add_field(name="Karma has been sent!",value=f"You have given `1` karma to {member.mention}\n{member.mention}'s total karma is now equal to {members[str(member.id)]}")

                with open('karma.json', 'w') as f:
                    json.dump(members, f, indent=4)

                await ctx.send(embed=embed)

            else:
                await ctx.send(f"{cross}You don't have enough karma to give it to someone!")
        else:
            await ctx.send(f"{cross} You cannot give karma to yourself!")

    @commands.command()
    async def karma(self, ctx, member : discord.Member=None):
        member = ctx.author if not member else member

        with open("karma.json","r") as f:
            members = json.load(f)

        #if len(str(members[str(member.id)])):
        memberKarma = members[str(member.id)]
        #else:
            #memberKarma = 0

        statuses = ['Severely Distrusted','Distrusted','Default','Trusted','Very Trusted']
        status = statuses[round((memberKarma/10)+2)]

        if memberKarma < -20:
            nextStatus = abs(memberKarma + 20)
        elif memberKarma < -10:
            nextStatus = abs(memberKarma + 10)
        elif memberKarma < 0:
            nextStatus = abs(memberKarma)
        elif memberKarma < 10:
            nextStatus = 10 - memberKarma
        elif memberKarma < 20:
            nextStatus = 20 - memberKarma
        else:
            nextStatus = "This is the highest level possible"

        embed = discord.Embed(colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
        embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
        embed.add_field(name="IC Discord Karma", value=f"\n{member.mention}'s karma: {memberKarma}\nStatus: {status}\nKarma to the next status: {nextStatus}")

        await ctx.send(embed=embed)

    @commands.command()
    async def remove(self, ctx, member : discord.Member):
        cross = self.client.get_emoji(798573872916070470)
        with open("karma.json","r") as f:
            members = json.load(f)

        authorKarma = members[str(ctx.author.id)]

        if member.id != ctx.author.id:
            if authorKarma >= 10:
                if str(member.id) in members:
                    members[str(member.id)] = members[str(member.id)] - 1
                else:
                    members[str(member.id)] = -1

                embed = discord.Embed(colour=discord.Colour.from_rgb(66, 135, 245), timestamp=ctx.message.created_at)
                embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                embed.add_field(name="Karma has been removed!",value=f"You have removed `1` karma from {member.mention}\n{member.mention}'s total karma is now equal to {members[str(member.id)]}")

                with open('karma.json', 'w') as f:
                    json.dump(members, f, indent=4)

                await ctx.send(embed=embed)

            else:
                await ctx.send(f"{cross} You don't have enough karma to remove it from someone!")
        else:
            await ctx.send(f"{cross} You cannot remove karma from yourself!")

def setup(client):
    client.add_cog(Commands(client))