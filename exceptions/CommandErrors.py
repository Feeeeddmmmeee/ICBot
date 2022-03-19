from dis import disco
from discord.ext.commands.errors import CommandError
import discord

class GuildNotValidated(CommandError):
    def __init__(self):
        super().__init__("This command isn't available in your guild!")

class InvalidRule(CommandError):
    def __init__(self):
        super().__init__("There's no such rule!")

class InvalidGameMode(CommandError):
    def __init__(self):
        super().__init__("There's no such game mode!")

class VerificationError(CommandError):
    def __init__(self, message: str, member: discord.Member, guild: discord.Guild, channel):
        self.member, self.guild, self.channel = member, guild, channel
        super().__init__("Verification Error: " + message)