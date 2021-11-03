import discord, os
from discord.ext import commands
from dotenv import load_dotenv
from pathlib import Path

intents = discord.Intents.all()
discord.member = True
discord.guild = True
discord.reaction = True

dotenv_path = Path(__file__.replace("main.py", "/config/token.env"))

load_dotenv(dotenv_path = dotenv_path)
TOKEN = os.getenv('TOKEN')

client = commands.Bot(command_prefix = ['ic ', 'IC ', 'Ic ', 'iC '], intents = intents, allowed_mentions=discord.AllowedMentions(everyone=False))

client.remove_command('help')
client.owner_id = 585115156757872653

@client.before_invoke
async def typing(ctx):
    if not ctx.command.name in ['verify']:
        await ctx.trigger_typing()

@client.event
async def on_ready():
    print(f">> Logged in as {client.user}")

    activity = discord.Activity(name="Intersection Controller", type=discord.ActivityType.playing)
    await client.change_presence(status=discord.Status.online, activity=activity)

for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
        client.load_extension(f'commands.{filename[:-3]}')

for filename in os.listdir('./events'):
    if filename.endswith('.py'):
        client.load_extension(f'events.{filename[:-3]}')

client.run(TOKEN)