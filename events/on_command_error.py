import discord, datetime
from discord.ext import commands

class On_command_error(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandOnCooldown):
            command = self.client.get_command('suggest')

            mins = str(datetime.timedelta(seconds=command.get_cooldown_retry_after(ctx)))
            mins = mins.split(":")[1]

            if mins.startswith("0"): mins.replace("0", "")
            mins = int(mins) + 1

            await ctx.reply(f"Please wait {mins} more minutes before running this command again!", mention_author=False)

        elif isinstance(error, commands.errors.CommandNotFound):
            pass

        else:
            embed = discord.Embed(
                color = discord.Color.from_rgb(255, 13, 0),
                title = ":x: Command raised an exception!",
                timestamp = ctx.message.created_at,
                description = f"```{error}```"
            )
            embed.add_field(name="Please contact the developer!", value="DM or mention Feeeeddmmmeee#7784.")
            embed.set_footer(text=str(ctx.author), icon_url=ctx.author.avatar_url)

            await ctx.reply(embed=embed, mention_author=False)
        

def setup(client):
    client.add_cog(On_command_error(client))