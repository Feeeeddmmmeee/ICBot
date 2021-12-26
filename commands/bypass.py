import discord, json
from discord.ext import commands

from exceptions.errors import GuildNotValidated

class Bypass(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_guild_permissions(manage_roles = True)
    async def bypass(self, ctx, member: discord.Member):
        with open("config/validguilds.json", "r") as config:
            validated  = ctx.guild.id in json.load(config)

        if not validated: raise GuildNotValidated

        player = discord.utils.get(ctx.guild.roles,name="IC player")

        await member.add_roles(player)

        logs = discord.utils.get(ctx.guild.channels, name="verification-logs")

        logged = discord.Embed(
            description = f"{member.mention} {member}",
            timestamp = ctx.message.created_at,
            color = discord.Color.green()
        )

        logged.set_author(name="User Bypassed", icon_url=member.avatar_url)
        logged.add_field(name="Bypassed By", value=str(ctx.author))

        await logs.send(embed = logged)  

        await ctx.reply(f"Successfully bypassed {member.mention}!", mention_author=False, allowed_mentions = discord.AllowedMentions.none())

def setup(client):
    client.add_cog(Bypass(client))