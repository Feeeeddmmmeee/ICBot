import discord
import datetime
import random
import json
import os
import asyncio
import requests
from discord.utils import get
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
    async def host(self, ctx, *, description):
        queue = self.client.get_channel(790556584778530897)#790556584778530897
        cross = self.client.get_emoji(798573872916070470)
        tick = self.client.get_emoji(798573863184236574)
        with open("config.json", "r") as f:
            config = json.load(f)

        if ctx.guild.id in config["validIds"]:
            with open('competitions.json','r') as f:
                competitions = json.load(f)

            competitions.append({"id": len(competitions)+1, "host": ctx.author.id, "description": description, "submissions":[],"voting": False, "winner": None, "approved": False})

            with open('competitions.json','w') as f:
                json.dump(competitions, f, indent=4)

            embed = discord.Embed(
                colour=discord.Colour.from_rgb(66, 135, 245),
                description=f"{ctx.author.mention} has submitted a competition!\n\nDescription: {description}\n\n[[Message Link]](https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{ctx.message.id})",
                timestamp=ctx.message.created_at
                )
            embed.set_footer(text=f"ID: {len(competitions)} • ic approve <id> to approve")

            await queue.send(embed=embed)

            await ctx.send(f"{tick} Successfully submitted your competition (ID: {len(competitions)})!")
        else:
            await ctx.send(f"{cross} This commands isn't available in your server!")

    @commands.command()
    async def submit(self, ctx, id, *, name):
        cross = self.client.get_emoji(798573872916070470)
        tick = self.client.get_emoji(798573863184236574)
        with open("config.json", "r") as f:
            config = json.load(f)

        if ctx.guild.id in config["validIds"]:
            with open('competitions.json','r') as f:
                competitions = json.load(f)
            if competitions[int(id)-1]["approved"] == True:
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
            else:
                await ctx.send(f"{cross} This competition has not been approved yet!")
        else:
            await ctx.send(f"{cross} This commands isn't available in your server!")

    @commands.command()
    async def voting(self, ctx, id):
        cnl = self.client.get_channel(676771002021314591)
        cross = self.client.get_emoji(798573872916070470)
        tick = self.client.get_emoji(798573863184236574)
        with open("config.json", "r") as f:
            config = json.load(f)

        if ctx.guild.id in config["validIds"]:
            with open('competitions.json','r') as f:
                competitions = json.load(f)
            if competitions[int(id)-1]["approved"] == True:
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

                                msg = await cnl.send(embed=embed)
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
            else:
                await ctx.send(f"{cross} This competition has not been approved yet!")
        else:
            await ctx.send(f"{cross} This commands isn't available in your server!")

    @commands.command(aliases=['finish'])
    async def end(self, ctx, id):
        announcement = self.client.get_channel(677491834670284801)#677491834670284801
        cross = self.client.get_emoji(798573872916070470)
        tick = self.client.get_emoji(798573863184236574)
        with open("config.json", "r") as f:
            config = json.load(f)

        if ctx.guild.id in config["validIds"]:
            with open('competitions.json','r') as f:
                competitions = json.load(f)
            if competitions[int(id)-1]["approved"] == True:
                if competitions[int(id)-1]["voting"] == True:
                    if competitions[int(id)-1]["winner"] == None:
                        if ctx.author.id == competitions[int(id)-1]["host"]:

                            order = []

                            for submission in competitions[int(id)-1]["submissions"]:

                                msgId = submission["messageId"]
                                cache_msg = await ctx.channel.fetch_message(msgId)
                                #await ctx.send(cache_msg.reactions.emoji.count)

                                reaction = cache_msg.reactions[0]

                                order.append((msgId, reaction.count))
                                
                            competitions[int(id)-1]["voting"] = False

                            sortedOrder = sorted(order, key=lambda k: k[1], reverse=True)
                            
                            winnerMsgId = sortedOrder[0][0]

                            for submission in competitions[int(id)-1]["submissions"]:
                                if submission["messageId"] == winnerMsgId:
                                    winner = ctx.guild.get_member(submission['author'])

                            oldone = ctx.guild.get_member(competitions[int(id)-2]["winner"])

                            win = discord.utils.get(ctx.guild.roles,name="Winners Of Campaign")

                            if competitions[int(id)-2]["winner"]:
                                await oldone.remove_roles(win)
                            await winner.add_roles(win)

                            competitions[int(id)-1]["winner"] = winner.id

                            embed=discord.Embed(
                                colour=discord.Colour.from_rgb(66, 135, 245),
                                description=f"{winner.mention} has won the competition with {sortedOrder[0][1]-1} votes!",
                                timestamp=ctx.message.created_at
                                )
                            embed.set_footer(text=f"Competition ID: {id}")
                            await announcement.send(embed=embed)

                            with open('competitions.json','w') as f:
                                json.dump(competitions, f, indent=4)
                        else:
                            await ctx.send(f"{cross} Only the competition host can do this!")
                    else:
                        await ctx.send(f"{cross} This competition has already ended!")
                else:
                    await ctx.send(f"{cross} The voting has not started/already ended!")
            else:
                await ctx.send(f"{cross} This competition has not been approved yet!")
        else:
            await ctx.send(f"{cross} This commands isn't available in your server!")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def approve(self, ctx, id):
        announcement = self.client.get_channel(677491834670284801)#677491834670284801
        cross = self.client.get_emoji(798573872916070470)
        tick = self.client.get_emoji(798573863184236574)
        with open("config.json", "r") as f:
            config = json.load(f)

        if ctx.guild.id in config["validIds"]:
            with open('competitions.json','r') as f:
                competitions = json.load(f)
            if competitions[int(id)-1]["approved"] == False:

                competitions[int(id)-1]["approved"] = True

                with open('competitions.json','w') as f:
                    json.dump(competitions, f, indent=4)

                announcementMsg = discord.Embed(
                    colour=discord.Colour.from_rgb(66, 135, 245),
                    description=f"{competitions[int(id)-1]['description']}",
                    timestamp=ctx.message.created_at
                    )
                announcementMsg.set_footer(text=f"ID: {competitions[int(id)-1]['id']} • Author: {self.client.get_user(competitions[int(id)-1]['host'])}")

                await announcement.send(get(ctx.guild.roles, name='Contestant').mention)
                await announcement.send(embed=announcementMsg)

            else:
                await ctx.send(f"{cross} This competition has already been approved!")
        else:
            await ctx.send(f"{cross} This commands isn't available in your server!")

        
    @commands.command(aliases=['comp'])
    async def competition(self, ctx, id):
        cross = self.client.get_emoji(798573872916070470)
        with open("competitions.json", "r")as f:
            comps = json.load(f)

        desc = ""
        nr=0

        if comps[int(id)-1]["winner"] != None:
            for submission in comps[int(id)-1]["submissions"]:
                desc = desc + f"<@{submission['author']}>"
                nr = nr+1
                if nr < len(comps[int(id)-1]["submissions"]):
                    desc = desc + ", "

            embed=discord.Embed(
                colour=discord.Colour.from_rgb(66, 135, 245),
                timestamp=ctx.message.created_at
                )
            embed.set_footer(text=f"ID: {id} • Host: {comps[int(id)-1]['host']}")
            embed.add_field(name="Host:", value=f'<@{comps[int(id)-1]["host"]}>')
            embed.add_field(name="Winner:", value=f'<@{comps[int(id)-1]["winner"]}>')
            embed.add_field(name="Contestants:", value=desc)
            embed.add_field(name="Competition Description:",value=comps[int(id)-1]["description"],inline=False)

            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{cross} This competition has not ended yet!")
        

def setup(client):
    client.add_cog(Commands(client))