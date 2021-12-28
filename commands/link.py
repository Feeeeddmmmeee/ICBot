import discord, intersection, json
from discord.ext import commands
from libs import asqlite

from exceptions.CommandErrors import GuildNotValidated

class Link(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_guild_permissions(manage_roles = True)
    async def link(self, ctx, user : discord.User, object_id):

        with open("config/ValidGuilds.json", "r") as config:
            validated  = ctx.guild.id in json.load(config)

        if not validated: raise GuildNotValidated

        ic_user = intersection.user.get_details_for_user(userId = object_id)

        async with asqlite.connect("database.sqlite") as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS accounts (discord_id INTEGER, ic_id INTEGER)")
                await cursor.execute(f"SELECT ic_id FROM accounts WHERE discord_id = {user.id}")
                data = await cursor.fetchone()
            
                if not data:
                    await cursor.execute(f"INSERT INTO accounts(discord_id, ic_id) VALUES({user.id}, {ic_user.objectId})")
                else:
                    await cursor.execute(f"UPDATE accounts SET ic_id = {ic_user.objectId} WHERE discord_id = {user.id}")

                await conn.commit()

        await ctx.reply(f"Successfully linked an account to {user.mention}!", mention_author = False, allowed_mentions = discord.AllowedMentions.none())   

        logs = discord.utils.get(ctx.guild.channels, name="verification-logs")

        logged = discord.Embed(
            description = f"{user.mention} {user}",
            timestamp = ctx.message.created_at,
            color = discord.Color.green()
        )

        logged.set_author(name="Account Linked", icon_url=user.avatar_url)
        logged.add_field(name="ID", value=object_id)
        logged.add_field(name="Linked By", value=str(ctx.author))

        await logs.send(embed = logged)       

        async with asqlite.connect("database.sqlite") as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f'SELECT * FROM accounts')
                amount_of_users = await cursor.fetchall()

        activity = discord.Activity(name=f"{len(amount_of_users)} Linked Accounts", type=discord.ActivityType.watching)
        await self.client.change_presence(status=discord.Status.online, activity=activity)

def setup(client):
    client.add_cog(Link(client))