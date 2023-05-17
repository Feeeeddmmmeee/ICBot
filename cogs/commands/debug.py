import discord, ast, asyncio, tl3api
from discord.ext import commands
import aiosqlite
from discord import app_commands
from main import logger, MyClient

def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
        if isinstance(body[-1], ast.Expr):
            body[-1] = ast.Return(body[-1].value)
            ast.fix_missing_locations(body[-1])

        # for if statements, we insert returns into the body and the orelse
        if isinstance(body[-1], ast.If):
            insert_returns(body[-1].body)
            insert_returns(body[-1].orelse)

        # for with blocks, again we insert returns into the body
        if isinstance(body[-1], ast.With):
            insert_returns(body[-1].body)

SEND_EMBED = True
class Modal(discord.ui.Modal, title="Debug"):
    def __init__(self, client: MyClient, *args, **kwargs):
        self.client = client
        super().__init__(*args, **kwargs)

    code = discord.ui.TextInput(label="code", style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):
        logger.debug("Executing input")
        await interaction.response.defer()
        fn_name = "_eval_expr"
        code = str(self.code)
        code = code.strip("` ")

        # add a layer of indentation
        code = "\n".join(f"    {i}" for i in code.splitlines())

        # wrap in async def body
        body = f"async def {fn_name}():\n{code}"

        if SEND_EMBED:
            embed = discord.Embed(
                title=f"Executing Input",
                description=f"```py\n{body}```",
                color=discord.Color.green()
            )
            
            await interaction.followup.send(embed=embed)

        parsed = ast.parse(body)
        body = parsed.body[0].body

        insert_returns(body)

        async def send(*args, **kwargs):
            await interaction.followup.send(*args, **kwargs)

        env = {
            'interaction': interaction,
            'discord': discord,
            'commands': commands,
            '__import__': __import__,
            'self': self,
            'asyncio': asyncio,
            'tl3api': tl3api,
            'aiosqlite': aiosqlite,
            'logger': logger,
            'send': send,
            'SEND_EMBED': SEND_EMBED,
        }
        exec(compile(parsed, filename="<ast>", mode="exec"), env)

        try:
            await eval(f"{fn_name}()", env)

        except Exception as error:
            await interaction.followup.send(str(error), ephemeral=True)

class Debug(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.send_embed = True

    @app_commands.command(name="debug", description="Executes code. Owner only.")
    async def debug(self, interaction: discord.Interaction):
        if interaction.user.id != self.client.owner_id:
            await interaction.response.send_message("This command can only be ran by the bot owner.", ephemeral=True)
            return

        await interaction.response.send_modal(Modal(self.client))

async def setup(client: commands.Bot):
    if client.debug:
        await client.add_cog(Debug(client), guilds=[discord.Object(id=744653826799435806)])
    else:
        await client.add_cog(Debug(client))
