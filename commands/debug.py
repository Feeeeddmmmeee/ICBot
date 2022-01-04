import discord, ast, asyncio, intersection
from discord.ext import commands
from matplotlib import pyplot as plt
from libs import asqlite

async def database(what):
    async with asqlite.connect("database.sqlite") as conn:
        async with conn.cursor() as cursor:

            await cursor.execute(what)

            toreturn = await cursor.fetchall()

    return toreturn


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

class Debug(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.send_embed = True

    @commands.is_owner()
    @commands.command(aliases = ['eval', 'ev'])
    async def debug(self, ctx, *, code):
        fn_name = "_eval_expr"

        code = code.strip("` ")

        # add a layer of indentation
        code = "\n".join(f"    {i}" for i in code.splitlines())

        # wrap in async def body
        body = f"async def {fn_name}():\n{code}"

        if self.send_embed:
            embed = discord.Embed(
                title=f"Executing Input",
                description=f"```py\n{body}```",
                color=discord.Color.green()
            )
            
            await ctx.reply(embed=embed, mention_author=False)

        parsed = ast.parse(body)
        body = parsed.body[0].body

        insert_returns(body)

        env = {
            'bot': ctx.bot,
            'discord': discord,
            'commands': commands,
            'ctx': ctx,
            '__import__': __import__,
            'self': self,
            'database': database,
            'asyncio': asyncio,
            "plt": plt,
            'intersection': intersection,
            'asqlite': asqlite,
        }
        exec(compile(parsed, filename="<ast>", mode="exec"), env)

        try:
            await eval(f"{fn_name}()", env)

        except Exception as error:
            await ctx.send(str(error))

def setup(client):
    client.add_cog(Debug(client))