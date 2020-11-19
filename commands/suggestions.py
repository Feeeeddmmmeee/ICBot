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
    async def suggest(self, ctx, *, suggestion):
        embed = discord.Embed(
            colour=discord.Colour.from_rgb(66, 135, 245),
            timestamp=ctx.message.created_at,
            description=suggestion,
        )
        embed.set_footer(text=f"Suggested by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

        channel = ctx.bot.get_channel(600465489508171776)
        like = ctx.bot.get_emoji(759059895424909380)
        dislike = ctx.bot.get_emoji(759060520455766036)
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

def setup(client):
    client.add_cog(Commands(client))