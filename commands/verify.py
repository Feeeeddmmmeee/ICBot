from datetime import datetime
import discord, json, random, asyncio, intersection
from discord.ext import commands
from main import guild_id
from libs import asqlite

from exceptions.CommandErrors import GuildNotValidated, VerificationError

class Verify(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def verify(self, ctx: commands.Context, member: discord.User = None):
        if not member: member = ctx.author
        elif not ctx.author.guild_permissions.manage_messages and not member == ctx.author: raise commands.errors.MissingPermissions(["manage_roles"])
        channel = member.dm_channel

        if ctx.channel != member.dm_channel:

            with open("config/ValidGuilds.json", "r") as config:
                validated  = ctx.guild.id in json.load(config)

            if not validated: raise GuildNotValidated
            channel = ctx.channel

        await ctx.message.add_reaction('📬')

        guild = self.client.get_guild(guild_id)
        member = guild.get_member(member.id)

        try:
            logs = discord.utils.get(guild.channels, name="verification-logs")

            logged = discord.Embed(
                description = f"{member.mention} {member}",
            )

            chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M']
            name = ""

            for i in range(6):
                name = name + random.choice(chars)

            embed = discord.Embed(
                title = ":link: Account Verification",
                description = "I'm **Intersection Controller**, a Discord bot responsible for connecting people's Discord and IC accounts to allow them to view IC information on Discord. If you run into any problems please contact our administrator team in <#709891493737005157>. The **#numbers** thing under your profile is your ID (without the hashtag)\n\nIn order to see the rest of our server you will need to go through the verification process. To do so first send me your **Intersection Controller account ID** (It's visible on your profile page in the game, the one other people can view through comments/maps)",
                color = discord.Color.blue(),
                timestamp = datetime.now()#ctx.message.created_at
            )

            embed.set_footer(text = member.name, icon_url = member.avatar_url)
            embed.set_image(url="https://media.discordapp.net/attachments/879324217462632478/919997649439055882/Untitled.png")

            await member.send(embed = embed)

            def check(message):
                return message.author == member and message.channel == member.dm_channel

            try:
                msg = await self.client.wait_for("message", timeout = 5 * 60.0, check = check)
            
            except asyncio.TimeoutError:
                await member.send("You didn't respond in time so I have stopped the process. To restart verification type `ic verify`")
                logged.set_author(name="Verification Timed Out", icon_url=member.avatar_url)
                logged.color = discord.Color.red()
                logged.timestamp=datetime.now()

                await logs.send(embed=logged)
                return

            if not "#" in msg.content: message = msg.content
            else: message  = msg.content.replace("#", "")

            try:
                id = int(message)

            except:
                await member.send("Invalid ID format!")
                logged.set_author(name="Verification Failed - Invalid ID", icon_url=member.avatar_url)
                logged.color = discord.Color.red()

                logged.add_field(name="Presumed ID", value=message)
                logged.add_field(name="Code", value=name)
                logged.timestamp=datetime.now()

                await logs.send(embed=logged)
                return

            logged.set_author(name="Verification Started", icon_url=member.avatar_url)
            logged.color = discord.Color.green()

            logged.add_field(name="Presumed ID", value=id)
            logged.add_field(name="Code", value=name)
            logged.timestamp=datetime.now()

            await logs.send(embed=logged)

            user = intersection.user.get_details_for_user(userId=id)

            if(not user.maps):
                embed = discord.Embed(
                    title = f":link: Account Verification - {user.name}",
                    description = "Now, in order to be verified, you'll need to **upload a new map** with the name I'll send you in my next message (just copy and paste it).\n\nRemember that you need to upload the map on the account you have previously posted the ID of or otherwise I will be unable to verify you! If you don't do so within 5 minutes I will automatically stop the process. Make sure not to delete the map until I verify you!",
                    color = discord.Color.blue(),
                    timestamp = datetime.now()
                )

                embed.set_footer(text = member.name, icon_url = member.avatar_url)

                await member.send(embed=embed)
                await member.send(name)

                for i in range(15):
                    await asyncio.sleep(20)
                    try:
                        map = intersection.map.list_maps_by_user(userId = id, result = 1)[0]

                        if map.name == name: break
                    except:
                        pass
                
                if(map.name == name):
                    embed = discord.Embed(
                        title = f":link: Account Verification - {user.name}",
                        description = "You have been successfully verified. Now, go visit our server and try out a bunch of awesome commands! You can type `ic profile @member` to view their IC user information or just run `ic profile` to view yours.\n\nIf you want to delete the map you can do it now.",
                        color = discord.Color.blue(),
                        timestamp = datetime.now()
                    )

                    embed.set_footer(text = member.name, icon_url = member.avatar_url)

                    player = discord.utils.get(guild.roles,name="IC player")

                    async with asqlite.connect("database.sqlite") as conn:
                        async with conn.cursor() as cursor:

                            await cursor.execute("CREATE TABLE IF NOT EXISTS accounts (discord_id INTEGER, ic_id INTEGER)")
                            await cursor.execute(f"SELECT ic_id FROM accounts WHERE discord_id = {member.id}")
                            data = await cursor.fetchone()
                                
                            if not data:
                                await cursor.execute(f"INSERT INTO accounts(discord_id, ic_id) VALUES({member.id}, {id})")
                            else:
                                await cursor.execute(f"UPDATE accounts SET ic_id = {id} WHERE discord_id = {member.id}")

                            await conn.commit()

                    await member.add_roles(player, reason = f"an IC account was linked to the user. ID: {id}")

                    await member.send(embed = embed)

                    logged.set_author(name="Verification Succeeded - Map", icon_url=member.avatar_url)
                    logged.color = discord.Color.green()
                    logged.timestamp=datetime.now()

                    await logs.send(embed=logged)

                    async with asqlite.connect("database.sqlite") as conn:
                        async with conn.cursor() as cursor:
                            await cursor.execute(f'SELECT * FROM accounts')
                            amount_of_users = await cursor.fetchall()

                    activity = discord.Activity(name=f"{len(amount_of_users)} Linked Accounts", type=discord.ActivityType.watching)
                    await self.client.change_presence(status=discord.Status.online, activity=activity)

                else:
                    logged.set_author(name="Verification Failed - Map", icon_url=member.avatar_url)
                    logged.color = discord.Color.red()
                    logged.timestamp=datetime.now()

                    await logs.send(embed=logged)
                    await member.send(f"Your latest map's name ({map.name}) doesn't match the verification name ({name})! I have stopped the verification process. Type `ic verify` if you wish to restart.")

            else:
                embed = discord.Embed(
                    title = f":link: Account Verification - {user.name}",
                    description = f"Now, in order to be verified, you'll need to **post a new comment** under your **latest map** ({intersection.map.list_maps_by_user(userId = id, result = 1)[0].name}) with just the content of my next message (just copy and paste it).\n\nRemember that you need to post the comment with the account you have previously posted the ID of or otherwise I will be unable to verify you! If you don't do so within 5 minutes I will automatically stop the process. Make sure not to delete the comment until I verify you!",
                    color = discord.Color.blue(),
                    timestamp = ctx.message.created_at
                )

                embed.set_footer(text = member.name, icon_url = member.avatar_url)

                await member.send(embed=embed)
                await member.send(name)

                for i in range(15):
                    await asyncio.sleep(20)
                    try:
                        comment = intersection.map.list_maps_by_user(userId = id, result = 1)[0].get_comments(limit=1)[0]

                        if comment.comment == name and comment.user == id: break
                    except:
                        pass
                
                if(comment.comment == name and comment.user == id):
                    embed = discord.Embed(
                        title = f":link: Account Verification - {user.name}",
                        description = "You have been successfully verified. Now, go visit our server and try out a bunch of awesome commands! You can type `ic profile @member` to view someone's IC user information or just run `ic profile` with no arguments to view yours.\n\nIf you want to delete the comment you can do it now.",
                        color = discord.Color.blue(),
                        timestamp = ctx.message.created_at
                    )

                    embed.set_footer(text = member.name, icon_url = member.avatar_url)

                    player = discord.utils.get(guild.roles,name="IC player")

                    async with asqlite.connect("database.sqlite") as conn:
                        async with conn.cursor() as cursor:

                            await cursor.execute("CREATE TABLE IF NOT EXISTS accounts (discord_id INTEGER, ic_id INTEGER)")
                            await cursor.execute(f"SELECT ic_id FROM accounts WHERE discord_id = {member.id}")
                            data = await cursor.fetchone()
                                
                            if not data:
                                await cursor.execute(f"INSERT INTO accounts(discord_id, ic_id) VALUES({member.id}, {id})")
                            else:
                                await cursor.execute(f"UPDATE accounts SET ic_id = {id} WHERE discord_id = {member.id}")

                            await conn.commit()

                    await member.add_roles(player, reason = f"an IC account was linked to the user. ID: {id}")

                    await member.send(embed = embed)

                    logged.set_author(name="Verification Succeeded - Comment", icon_url=member.avatar_url)
                    logged.color = discord.Color.green()
                    logged.timestamp=datetime.now()

                    await logs.send(embed=logged)

                    async with asqlite.connect("database.sqlite") as conn:
                        async with conn.cursor() as cursor:
                            await cursor.execute(f'SELECT * FROM accounts')
                            amount_of_users = await cursor.fetchall()

                    activity = discord.Activity(name=f"{len(amount_of_users)} Linked Accounts", type=discord.ActivityType.watching)
                    await self.client.change_presence(status=discord.Status.online, activity=activity)

                else:
                    logged.set_author(name="Verification Failed - Comment", icon_url=member.avatar_url)
                    logged.color = discord.Color.red()
                    logged.timestamp=datetime.now()

                    await logs.send(embed=logged)
                    await member.send(f"The latest comment under **{intersection.map.list_maps_by_user(userId = id, result = 1)[0].name}** ({intersection.map.list_maps_by_user(userId = id, result = 1)[0].get_comments(limit=1)[0]}) doesn't match the verification code ({name})! I have stopped the verification process. Type `ic verify` if you wish to restart.")

        except Exception as e:
            raise VerificationError(str(e), member, guild, channel)


def setup(client):
    client.add_cog(Verify(client))