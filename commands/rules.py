import discord, json
from discord.ext import commands

from exceptions.CommandErrors import InvalidRule

def check_number(number):
    if number.lower().replace(" ", "") in ["bans", "permanent", "permanentban", "banpermanent", "permanentbans", "banspermanent"]:
        number = "ban"
    elif number.lower().replace(" ", "") in ["mod", "mods", "admin", "admins", "administration", "administrator", "administrators", "moderator", "moderators"]:
        number = "moderation"
    elif number.lower().replace(" ", "") in ["one", "uno", "respect", "discrimination", "respectanddiscimination", "discrimination and respect"]: number = "1"
    elif number.lower().replace(" ", "") in ["two", "personalinfo", "info", "personal", "personal information", "infopersonal", "informationpersonal"]: number = "2"
    elif number.lower() in ["three", "nsfw", "lewd"]: number = "3"
    elif number.lower().replace(" ", "") in ["four", "spam", "channels", "usingchannels", "channelusage"]: number = "4"
    elif number.lower() in ["five", "ad", "ads", "advertisement", "advertisements"]: number = "5"
    elif number.lower() in ["six", "drugs"]: number = "6"
    elif number.lower().replace(" ", "") in ["seven", "loophole", "loopholes", "alt", "alts", "altaccount", "altaccounts"]: number = "7"

    if not number in ["1", "2", "3", "4", "5", "6", "7", "ban", "moderation"]: raise InvalidRule

    return number

class Rules(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ["rule"])
    async def rules(self, ctx, *, number: str):
        with open("config/rules.json", "r") as f:
            file = json.load(f)

        number = check_number(number)
            
        embed = discord.Embed(
            colour = discord.Colour.from_rgb(66, 135, 245),
            title = file[number]["title"],
            description = file[number]["desc"]
        )

        await ctx.reply(embed=embed, mention_author=False)

def setup(client):
    client.add_cog(Rules(client))