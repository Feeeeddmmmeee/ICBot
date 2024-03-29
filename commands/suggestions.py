import discord
import datetime
import random
import json
import os
import asyncio
import requests
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, MissingPermissions

def isNotBanned(ctx):
    with open('banned_users.json', 'r') as f:
        banned = json.load(f)

    if str(ctx.author.id) in banned:
        return False
    else:
        return True

class Commands(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.check(isNotBanned)
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def suggest(self, ctx, *, suggestion):
        with open("config.json", "r") as f:
            config = json.load(f)
        cross = self.client.get_emoji(798573872916070470)
        if ctx.guild.id in config["validIds"]:
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(66, 135, 245),
                timestamp=ctx.message.created_at,
                description=suggestion,
            )
            embed.set_footer(text=f"Suggested by {ctx.author}", icon_url=ctx.author.avatar_url)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

            if len(ctx.message.attachments):
                attachment = ctx.message.attachments[0]
                embed.set_image(url = attachment.url)

            channel = ctx.bot.get_channel(600465489508171776)
            like = self.client.get_emoji(759059895424909380)
            dislike = self.client.get_emoji(759060520455766036)
            await ctx.message.add_reaction('📬')
            likes = await channel.send(embed=embed)
            await likes.add_reaction(like)
            await likes.add_reaction(dislike)
            await likes.add_reaction('🤍')

            dm = discord.Embed(
                colour=discord.Colour.from_rgb(66, 135, 245),
                title='Suggestion has been sent!'
            )
            dm.add_field(name="Hey! :wave:", value=f'Hey {ctx.author.mention}, your suggestion has been sent to the <#600465489508171776> channel so that people can like/dislike it!', inline=False)
            dm.add_field(name="Voting", value='Members are now allowed to vote for your suggestion!', inline=False)
            dm.add_field(name="Your suggestion was:", value=f'`{suggestion}`', inline=False)
            dm.set_footer(text=f'Replied to a suggestion by: {ctx.message.author}', icon_url=ctx.author.avatar_url)
            await ctx.author.send(embed=dm)
        else:
            await ctx.send(f"{cross} This commands isn't available in your server!")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def ban(self, ctx, member : discord.Member, *, reason = "reason not specified"):
        with open("config.json", "r") as f:
            config = json.load(f)
        cross = self.client.get_emoji(798573872916070470)
        tick = self.client.get_emoji(798573863184236574)
        if ctx.guild.id in config["validIds"]:
            with open('banned_users.json', 'r') as f:
                banned = json.load(f)
            if str(member.id) in banned:
                await ctx.send(f"{cross} This user is already banned!")
            else:
                banned[str(member.id)] = "BANNED"

                with open('banned_users.json', 'w') as f:
                    json.dump(banned, f, indent=4)
            
                await ctx.send(f"{tick} Successfully banned {member.mention}!")
                await member.send(f"You have been banned from suggesting things in Intersection Controller for `{reason}`")
        else:
            await ctx.send(f"{cross} This commands isn't available in your server!")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unban(self, ctx, member : discord.Member):
        with open("config.json", "r") as f:
            config = json.load(f)
        cross = self.client.get_emoji(798573872916070470)
        tick = self.client.get_emoji(798573863184236574)
        if ctx.guild.id in config["validIds"]:
            with open('banned_users.json', 'r') as f:
                banned = json.load(f)
            if str(member.id) in banned:

                banned.pop(str(member.id))

                with open('banned_users.json', 'w') as f:
                    json.dump(banned, f, indent=4)

                await ctx.send(f"{tick} Successfully unbanned {member.mention}!")
            else:
                await ctx.send(f"{cross} This user is not banned!")
        else:
            await ctx.send(f"{cross} This commands isn't available in your server!")


def setup(client):
    client.add_cog(Commands(client))