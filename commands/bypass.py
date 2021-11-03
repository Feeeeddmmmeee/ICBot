import discord, json
from discord.ext import commands

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_guild_permissions(manage_roles = True)
    async def bypass(self, ctx, member: discord.Member):
        with open("config/validguilds.json", "r") as config:
            validated  = ctx.guild.id in json.load(config)

        if not validated:
            embed = discord.Embed(
                description = f"<:neutral:905485648478228490> This command isn't available in your server!",
                color = discord.Color.blue()
            )

            await ctx.reply(embed=embed, mention_author=False)
            return

        player = discord.utils.get(member.guild.roles,name="IC player")
        unverified = discord.utils.get(member.guild.roles,name="Unverified")

        await member.add_roles(player)
        await member.remove_roles(unverified)

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
    client.add_cog(Help(client))