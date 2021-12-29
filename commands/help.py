import discord
from discord.ext import commands

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        embed = discord.Embed(
            title = "<:neutral:905485648478228490> Available Commands",
            description = "Type `ic help <command>` to get detailed information and syntax of a command!",
            color = discord.Color.blue()
        )

        embed.add_field(name="Admin / Developer", value="`ic link` `ic unlink` `ic debug` `ic bypass`", inline=False)
        embed.add_field(name="Profiles and Stuff", value="`ic profile` `ic verify` `ic map` `ic search` `getfrom`", inline=False)
        embed.add_field(name="Other", value="`ic cheats` `ic rules` `ic suggest` `ic help` `ic ping` `ic chart`", inline=False)


        await ctx.reply(embed = embed, mention_author=False)

    @help.command()
    async def chart(self, ctx):
        embed = discord.Embed(
            title = "<:neutral:905485648478228490> Chart Command",
            description = "Sends a follower chart based on users' raw followers/roles.\n\nSyntax 1: `ic chart roles` (fast)\nSyntax 2: `ic chart all <how to round (optional)>` (takes about 20 seconds to execute)",
            color = discord.Color.blue()
        )

        await ctx.reply(embed = embed, mention_author=False)

    @help.command()
    async def link(self, ctx):
        embed = discord.Embed(
            title = "<:neutral:905485648478228490> Link Command",
            description = "Links an Intersection Controller account to a Discord user!\n\nSyntax: `ic link <user> <id>`",
            color = discord.Color.blue()
        )

        await ctx.reply(embed = embed, mention_author=False)

    @help.command()
    async def unlink(self, ctx):
        embed = discord.Embed(
            title = "<:neutral:905485648478228490> Unlink Command",
            description = "Unlinks an Intersection Controller account from a Discord user!\n\nSyntax: `ic unlink <user>`",
            color = discord.Color.blue()
        )

        await ctx.reply(embed = embed, mention_author=False)

    @help.command()
    async def debug(self, ctx):
        embed = discord.Embed(
            title = "<:neutral:905485648478228490> Debug Command",
            description = "Executes input (Developer only).\n\nSyntax: `ic debug <code>`",
            color = discord.Color.blue()
        )

        await ctx.reply(embed = embed, mention_author=False)

    @help.command()
    async def bypass(self, ctx):
        embed = discord.Embed(
            title = "<:neutral:905485648478228490> Bypass Command",
            description = "Bypasses a user (verification command, used to only update a user's roles).\n\nSyntax: `ic bypass <user>`",
            color = discord.Color.blue()
        )

        await ctx.reply(embed = embed, mention_author=False)

    @help.command()
    async def profile(self, ctx):
        embed = discord.Embed(
            title = "<:neutral:905485648478228490> Profile Command",
            description = "Sends information about a Discord user's IC account (works only with linked accounts).\n\nSyntax: `ic profile <user>`",
            color = discord.Color.blue()
        )

        await ctx.reply(embed = embed, mention_author=False)

    @help.command()
    async def verify(self, ctx):
        embed = discord.Embed(
            title = "<:neutral:905485648478228490> Verify Command",
            description = "Starts the verification process for a user. Everyone can use the command, admins can additionally mention a user to verify.\n\nSyntax: `ic verify`",
            color = discord.Color.blue()
        )

        await ctx.reply(embed = embed, mention_author=False)

    @help.command()
    async def map(self, ctx):
        embed = discord.Embed(
            title = "<:neutral:905485648478228490> Map Command",
            description = "Sends IC map information. Can be used on both **verified Discord users** and **Intersection Controller IDs**.\n\nSyntax 1: `ic map <index> <user>`\nSyntax 2: `ic map <index> <ic id>`",
            color = discord.Color.blue()
        )

        await ctx.reply(embed = embed, mention_author=False)

    @help.command()
    async def search(self, ctx):
        embed = discord.Embed(
            title = "<:neutral:905485648478228490> Search Command",
            description = "Searches for a user with a given name.\n\nSyntax: `ic search <query>`",
            color = discord.Color.blue()
        )

        await ctx.reply(embed = embed, mention_author=False)

    @help.command()
    async def getfrom(self, ctx):
        embed = discord.Embed(
            title = "<:neutral:905485648478228490> Get from Command",
            description = "Sends information about a user with a matching name/ID.\n\nSyntax 1: `ic getfrom name <exact name>`\nSyntax 2: `ic getfrom id <id>`",
            color = discord.Color.blue()
        )

        await ctx.reply(embed = embed, mention_author=False)

    @help.command()
    async def cheats(self, ctx):
        embed = discord.Embed(
            title = "<:neutral:905485648478228490> Cheats Command",
            description = "Sends all the in-game cheat codes.\n\nSyntax: `ic cheats`",
            color = discord.Color.blue()
        )

        await ctx.reply(embed = embed, mention_author=False)

    @help.command()
    async def rules(self, ctx):
        embed = discord.Embed(
            title = "<:neutral:905485648478228490> Rules Command",
            description = "Sends information about a given server rules.\n\nSyntax: `ic rules <number>`",
            color = discord.Color.blue()
        )

        await ctx.reply(embed = embed, mention_author=False)
    
    @help.command()
    async def suggest(self, ctx):
        embed = discord.Embed(
            title = "<:neutral:905485648478228490> Suggest Command",
            description = "Sends your game suggestion to <#600465489508171776>.\n\nSyntax: `ic suggest <suggestion>`",
            color = discord.Color.blue()
        )

        await ctx.reply(embed = embed, mention_author=False)

    @help.command()
    async def ping(self, ctx):
        embed = discord.Embed(
            title = "<:neutral:905485648478228490> Suggest Command",
            description = "Sends the bot's ping.\n\nSyntax: `ic ping`",
            color = discord.Color.blue()
        )

        await ctx.reply(embed = embed, mention_author=False)

def setup(client):
    client.add_cog(Help(client))