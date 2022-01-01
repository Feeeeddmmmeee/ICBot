import discord, datetime
from discord.ext import commands
from exceptions.CommandErrors import GuildNotValidated, InvalidRule

class OnCommandError(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error: commands.errors.CommandError):
        if isinstance(error, commands.errors.CommandOnCooldown):
            command = self.client.get_command('suggest')

            mins = str(datetime.timedelta(seconds=command.get_cooldown_retry_after(ctx)))
            mins = mins.split(":")[1]

            if mins.startswith("0"): mins.replace("0", "")
            mins = int(mins) + 1

            embed = discord.Embed(
                description = f"<:neutral:905485648478228490> Please wait **{mins}** more minutes before running this command again!",
                color = discord.Color.blue()
            )

            await ctx.reply(embed=embed, mention_author=False)

        elif isinstance(error, commands.errors.CommandNotFound):
            pass

        elif isinstance(error, GuildNotValidated):
            embed = discord.Embed(
                description = f"<:neutral:905485648478228490> This command isn't available in your server!",
                color = discord.Color.blue()
            )

            await ctx.reply(embed=embed, mention_author=False)

        elif isinstance(error, InvalidRule):
            embed = discord.Embed(
                description = f"<:neutral:905485648478228490> There is no such rule!",
                color = discord.Color.blue()
            )

            await ctx.reply(embed=embed, mention_author = False)

        else:
            embed = discord.Embed(
                color = discord.Color.from_rgb(237, 50, 31),
                title = "<:error:905485648373370890> Command raised an exception!",
                timestamp = ctx.message.created_at,
                description = f"```{error}```"
            )
            embed.add_field(name="Please contact the developer!", value="DM or mention Feeeeddmmmeee#7784.")
            embed.set_footer(text=str(ctx.author), icon_url=ctx.author.avatar_url)

            await ctx.reply(embed=embed, mention_author=False)
        

def setup(client):
    client.add_cog(OnCommandError(client))