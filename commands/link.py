import discord, intersection, sqlite3, json
from discord.ext import commands

class Link(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_guild_permissions(manage_roles = True)
    async def link(self, ctx, user : discord.User, object_id):
        await ctx.trigger_typing()

        database = sqlite3.connect("database.sqlite")
        cursor = database.cursor()

        with open("config/validguilds.json", "r") as config:
            validated  = ctx.guild.id in json.load(config)

        if not validated:
            await ctx.reply(f"This commands isn't available in your server!", mention_author = False)
            return

        ic_user = intersection.user.get_details_for_user(userId = object_id)

        cursor.execute("CREATE TABLE IF NOT EXISTS accounts (discord_id INTEGER, ic_id INTEGER)")
        cursor.execute(f"SELECT ic_id FROM accounts WHERE discord_id = {user.id}")
        data = cursor.fetchone()
            
        if not data:
            cursor.execute(f"INSERT INTO accounts(discord_id, ic_id) VALUES({user.id}, {ic_user.objectId})")
        else:
            cursor.execute(f"UPDATE accounts SET ic_id = {ic_user.objectId} WHERE discord_id = {user.id}")

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

        database.commit()
        cursor.close()
        database.close()

def setup(client):
    client.add_cog(Link(client))