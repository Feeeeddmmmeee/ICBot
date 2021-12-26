from discord.ext.commands.errors import CommandError

class GuildNotValidated(CommandError):
    def __init__(self):
        super().__init__("This command isn't available in your guild!")