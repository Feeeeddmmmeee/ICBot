import discord, sqlite3, json, random, asyncio, intersection
from discord.ext import commands

class Verify(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def verify(self, ctx, member: discord.User = None):
        if not member: member = ctx.author
        elif not ctx.author.guild_permissions.manage_messages and not member == ctx.author: raise commands.errors.MissingPermissions(["manage_roles"])

        if ctx.channel != member.dm_channel:

            with open("config/validguilds.json", "r") as config:
                validated  = ctx.guild.id in json.load(config)

            if not validated:
                embed = discord.Embed(
                    description = f"<:neutral:905485648478228490> This command isn't available in your server!",
                    color = discord.Color.blue()
                )

                await ctx.reply(embed=embed, mention_author=False)
                return

        await ctx.message.add_reaction('📬')

        guild = self.client.get_guild(469861886960205824)
        member = guild.get_member(member.id)

        database = sqlite3.connect("database.sqlite")
        cursor = database.cursor()

        logs = discord.utils.get(guild.channels, name="verification-logs")

        logged = discord.Embed(
            description = f"{member.mention} {member}",
            timestamp = ctx.message.created_at
        )

        chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M']
        name = ""

        for i in range(6):
            name = name + random.choice(chars)

        embed = discord.Embed(
            title = ":link: Account Verification",
            description = "I'm **Intersection Controller**, a Discord bot responsible for connecting people's Discord and IC accounts to allow them to view IC information on Discord. If you run into any problems please contact our administrator team in <#709891493737005157>. The #numbers under your profile is your ID (without the hashtag)\n\nIn order to see the rest of our server you will need to go through the verification process. To do so first send me your **Intersection Controller account ID** (It's visible on your profile page in the game)\n\n:warning: **Do not share any of my messages unless you're sure what you're doing!**\nAnyone with this information will be able to link your account.",
            color = discord.Color.blue(),
            timestamp = ctx.message.created_at
        )

        embed.set_footer(text = member.name, icon_url = member.avatar_url)
        embed.set_image(url="https://media.discordapp.net/attachments/879324217462632478/905104265683533824/IMG_20211102_154055.jpg")

        await member.send(embed = embed)

        def check(message):
            return message.author == member and message.channel == member.dm_channel

        try:
            msg = await self.client.wait_for("message", timeout = 5 * 60.0, check = check)
        
        except asyncio.TimeoutError:
            await member.send("You didn't respond in time so I have stopped the process. To restart verification type `ic verify`")
            logged.set_author(name="Verification Timed Out", icon_url=member.avatar_url)
            logged.color = discord.Color.red()

            await logs.send(embed=logged)
            return

        try:
            id = int(msg.content)

        except:
            await member.send("Invalid ID format!")
            return

        logged.set_author(name="Verification Started", icon_url=member.avatar_url)
        logged.color = discord.Color.green()

        logged.add_field(name="Presumed ID", value=id)
        logged.add_field(name="Map Name", value=name)

        await logs.send(embed=logged)

        embed = discord.Embed(
            title = ":link: Account Verification",
            description = "Now, in order to be verified, you'll need to **upload a new map** with the name I'll send you in my next message (just copy and paste it).\n\nRemember that you need to upload the map on the account you have previously posted the ID of or otherwise I will be unable to verify you! If you don't do so within 5 minutes I will automatically stop the process. Make sure not to delete the map until I verify you!\n\n:warning: **Do not share any of my messages unless you're sure what you're doing!**\nAnyone with this information will be able to link your account.",
            color = discord.Color.blue(),
            timestamp = ctx.message.created_at
        )

        embed.set_footer(text = member.name, icon_url = member.avatar_url)

        await member.send(embed=embed)
        await member.send(name)

        for i in range(15):
            await asyncio.sleep(20)
            map = intersection.map.list_maps_by_user(userId = id, result = 1)[0]

            if map.name == name: break
        
        if(map.name == name):
            embed = discord.Embed(
                title = ":link: Account Verification",
                description = "You have been successfully verified. Now, go visit our server and try out a bunch of awesome commands! You can type `ic profile @member` to view their IC user information or just run `ic profile` to view yours.\n\nIf you want to delete the map you can do it now.\n\nThe verification map name I sent you isn't going to be used again so you can freely post it wherever you want now.",
                color = discord.Color.blue(),
                timestamp = ctx.message.created_at
            )

            embed.set_footer(text = member.name, icon_url = member.avatar_url)

            player = discord.utils.get(guild.roles,name="IC player")
            unverified = discord.utils.get(guild.roles,name="Unverified")

            cursor.execute("CREATE TABLE IF NOT EXISTS accounts (discord_id INTEGER, ic_id INTEGER)")
            cursor.execute(f"SELECT ic_id FROM accounts WHERE discord_id = {member.id}")
            data = cursor.fetchone()
                
            if not data:
                cursor.execute(f"INSERT INTO accounts(discord_id, ic_id) VALUES({member.id}, {id})")
            else:
                cursor.execute(f"UPDATE accounts SET ic_id = {id} WHERE discord_id = {member.id}")

            await member.add_roles(player)
            await member.remove_roles(unverified)

            await member.send(embed = embed)

            logged.set_author(name="Verification Succeeded", icon_url=member.avatar_url)
            logged.color = discord.Color.green()

            await logs.send(embed=logged)

        else:
            logged.set_author(name="Verification Failed", icon_url=member.avatar_url)
            logged.color = discord.Color.red()

            await logs.send(embed=logged)
            await member.send(f"Your latest map's name ({map.name}) doesn't match the verification name ({name})! I have stopped the verification process. Type `ic verify` if you wish to restart.")

        database.commit()
        cursor.close()
        database.close()

def setup(client):
    client.add_cog(Verify(client))