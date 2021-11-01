import discord, json, sqlite3
from discord.ext import commands

class Unlink(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_guild_permissions(manage_roles=True)
    async def unlink(self, ctx, user : discord.User):
        await ctx.trigger_typing()
        
        database = sqlite3.connect("database.sqlite")
        cursor = database.cursor()

        with open("config/validguilds.json", "r") as config:
            validated  = ctx.guild.id in json.load(config)

        if not validated:
            await ctx.reply(f"This commands isn't available in your server!", mention_author = False)
            return

        cursor.execute("CREATE TABLE IF NOT EXISTS accounts (discord_id INTEGER, ic_id INTEGER)")
        cursor.execute(f'SELECT ic_id FROM accounts WHERE discord_id = {user.id}')
        id = cursor.fetchone()
        cursor.execute(f"DELETE FROM accounts WHERE discord_id = {user.id}")

        await ctx.reply(f"Successfully unlinked an account from {user.mention}!", mention_author=False, allowed_mentions=discord.AllowedMentions.none())     

        logs = discord.utils.get(ctx.guild.channels, name="verification-logs")

        logged = discord.Embed(
            description = f"{user.mention} {user}",
            timestamp = ctx.message.created_at,
            color = discord.Color.red()
        )

        logged.set_author(name="Account Unlinked", icon_url=user.avatar_url)
        logged.add_field(name="ID", value=id[0])
        logged.add_field(name="Unlinked By", value=str(ctx.author))       

        await logs.send(embed=logged)

        database.commit()
        cursor.close()
        database.close()

def setup(client):
    client.add_cog(Unlink(client))