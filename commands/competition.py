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
    async def host(self, ctx, *, description):
        tick = self.client.get_emoji(798573863184236574)
    
        with open('competitions.json','r') as f:
            competitions = json.load(f)

        competitions.append({"id": len(competitions)+1, "host": ctx.author.id, "description": description, "submissions":[],"voting": False, "winner": None})

        with open('competitions.json','w') as f:
            json.dump(competitions, f, indent=4)

        await ctx.send(f"{tick} Successfully started your competition (ID: {len(competitions)})!")

    @commands.command()
    async def submit(self, ctx, id, *, name):
        cross = self.client.get_emoji(798573872916070470)
        tick = self.client.get_emoji(798573863184236574)

        with open('competitions.json','r') as f:
            competitions = json.load(f)

        if competitions[int(id)-1]["voting"] == False:
            if competitions[int(id)-1]["winner"] == None:
                if len(ctx.message.attachments):
                    attachment = ctx.message.attachments[0]
                    competitions[int(id)-1]["submissions"].append({"author": ctx.author.id, "name": name, "url": attachment.url, "messageId": None})

                    with open('competitions.json','w') as f:
                        json.dump(competitions, f, indent=4)

                    await ctx.send(f"{tick} Successfully added your submission!")
                else:
                    await ctx.send(f"{cross} You need to send an image of your map!")
            else:
                await ctx.send(f"{cross} This competition has already ended!")
        else:
            await ctx.send(f"{cross} The voting has already started!")

    @commands.command()
    async def voting(self, ctx, id):
        cross = self.client.get_emoji(798573872916070470)
        tick = self.client.get_emoji(798573863184236574)

        with open('competitions.json','r') as f:
            competitions = json.load(f)

        if competitions[int(id)-1]["voting"] == False:
            if competitions[int(id)-1]["winner"] == None:
                if ctx.author.id == competitions[int(id)-1]["host"]:
                    for item in competitions[int(id)-1]["submissions"]:
                        embed=discord.Embed(
                            colour=discord.Colour.from_rgb(66, 135, 245),
                            description=f"{self.client.get_user(item['author']).mention}'s submission, {item['name']}",
                            timestamp=ctx.message.created_at
                            )
                        embed.set_footer(text=f"Competition ID: {id}")
                        embed.set_image(url=item['url'])

                        msg = await ctx.send(embed=embed)
                        await msg.add_reaction("✅")
                        item["messageId"] = msg.id

                    competitions[int(id)-1]["voting"] = True
                    with open('competitions.json','w') as f:
                        json.dump(competitions, f, indent=4)

                else:
                    await ctx.send(f"{cross} Only the competition host can do this!")
            else:
                await ctx.send(f"{cross} This competition has already ended!")
        else:
            await ctx.send(f"{cross} The voting has already started!")

    @commands.command(aliases=['finish'])
    async def end(self, ctx, id):
        cross = self.client.get_emoji(798573872916070470)
        tick = self.client.get_emoji(798573863184236574)

        with open('competitions.json','r') as f:
            competitions = json.load(f)
        if competitions[int(id)-1]["voting"] == True:
            if competitions[int(id)-1]["winner"] == None:
                if ctx.author.id == competitions[int(id)-1]["host"]:

                    order = []

                    for submission in competitions[int(id)-1]["submissions"]:

                        msgId = submission["messageId"]
                        channel = self.client.get_channel(744653826799435809)
                        cache_msg = await channel.fetch_message(msgId)
                        #await ctx.send(cache_msg.reactions.emoji.count)

                        reaction = cache_msg.reactions[0]

                        order.append((msgId, reaction.count))
                        
                    competitions[int(id)-1]["voting"] = False

                    sortedOrder = sorted(order, key=lambda k: k[1], reverse=True)
                    
                    winnerMsgId = sortedOrder[0][0]

                    for submission in competitions[int(id)-1]["submissions"]:
                        if submission["messageId"] == winnerMsgId:
                            winner = self.client.get_user(submission['author'])

                    competitions[int(id)-1]["winner"] = winner.id
                    await ctx.send(winner.mention)
                    with open('competitions.json','w') as f:
                        json.dump(competitions, f, indent=4)
                else:
                    await ctx.send(f"{cross} Only the competition host can do this!")
            else:
                await ctx.send(f"{cross} This competition has already ended!")
        else:
            await ctx.send(f"{cross} The voting has not started yet!")

def setup(client):
    client.add_cog(Commands(client))