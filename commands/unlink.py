import discord, json
from discord.ext import commands
from libs import asqlite

from exceptions.errors import GuildNotValidated

class Unlink(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_guild_permissions(manage_roles=True)
    async def unlink(self, ctx, user : discord.Member):
        guild = ctx.guild

        with open("config/validguilds.json", "r") as config:
            validated  = ctx.guild.id in json.load(config)

        if not validated: raise GuildNotValidated

        async with asqlite.connect("database.sqlite") as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS accounts (discord_id INTEGER, ic_id INTEGER)")
                await cursor.execute(f'SELECT ic_id FROM accounts WHERE discord_id = ?', (user.id,))
                id = await cursor.fetchone()
                await cursor.execute(f"DELETE FROM accounts WHERE discord_id = ?", (user.id,))

                await conn.commit() 

        if not id:
            await ctx.reply(f"{user.mention}'s account is not linked!", mention_author=False, allowed_mentions=discord.AllowedMentions.none())
            return   

        logs = discord.utils.get(ctx.guild.channels, name="verification-logs")

        logged = discord.Embed(
            description = f"{user.mention} {user}",
            timestamp = ctx.message.created_at,
            color = discord.Color.red()
        )

        logged.set_author(name="Account Unlinked", icon_url=user.avatar_url)
        logged.add_field(name="ID", value=id[0])
        logged.add_field(name="Unlinked By", value=str(ctx.author))       

        await ctx.reply(f"Successfully unlinked an account from {user.mention}!", mention_author=False, allowed_mentions=discord.AllowedMentions.none()) 
        await logs.send(embed=logged)

        async with asqlite.connect("database.sqlite") as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f'SELECT * FROM accounts')
                amount_of_users = await cursor.fetchall()

        activity = discord.Activity(name=f"{len(amount_of_users)} Linked Accounts", type=discord.ActivityType.watching)
        await self.client.change_presence(status=discord.Status.online, activity=activity)

def setup(client):
    client.add_cog(Unlink(client))