# Created by Egehan Kılıçarslan on 30/12/2023
# This file is part of a project developed by Egehan Kılıçarslan.

import os
import hikari
import lightbulb
import miru

from utils.utils import Config
from pathlib import Path

SUCCESS_COLOR = Config().SUCCESS_COLOR
ERROR_COLOR = Config().ERROR_COLOR


class DiscordBotManager:
    """
    A class that manages the Discord bot application.

    Args:
        token (str): The token used to authenticate the bot.
        intents (Intents, optional): The intents to enable for the bot. Defaults to Intents.ALL.
        help (bool, optional): Whether to enable the help slash command. Defaults to True.
    """

    def __init__(self, token: str, intents: hikari.Intents, help: bool):
        self.bot = lightbulb.BotApp(token=token, intents=intents, help_slash_command=help)
        miru.install(self.bot)

    def load_extensions(self, extensions_directories: list[str]):
        """
        Load bot extensions from the specified directories.

        Args:
            extensions_directories (list[str]): A list of directories containing the bot extensions.
        """
        for directory in extensions_directories:
            self.bot.load_extensions_from(Path("extensions") / directory)

    @staticmethod
    def generate_error_embed(title: str, description: str):
        """
        Generate an error embed.

        Args:
            title (str, optional): The title of the error embed. Defaults to "ERROR".
            description (str, optional): The description of the error embed. Defaults to "ERROR".

        Returns:
            hikari.Embed: The generated error embed.
        """
        return hikari.Embed(title=title, description=description, color=ERROR_COLOR)

    def run(self, status: hikari.Status, activity: hikari.Activity):
        """
        Run the bot application.

        Args:
            status (Status, optional): The status of the bot. Defaults to Status.IDLE.
            activity (Activity, optional): The activity of the bot. Defaults to Activity(name="Activity", type=ActivityType.PLAYING).
        """
        self.bot.run(status=status, activity=activity)


if __name__ == "__main__":
    if os.name != "nt":
        import uvloop

        uvloop.install()

    # Configuration
    directories = ["test"] #Enter your extension forder names
    token = Config().TOKEN

    # Bot Initialization
    discord_bot_manager = DiscordBotManager(token=token, intents=hikari.Intents.ALL, help=True)
    discord_bot_manager.load_extensions(directories)

    # Event Handler for Command Errors
    @discord_bot_manager.bot.listen(lightbulb.CommandErrorEvent)
    async def on_command_error(event: lightbulb.CommandErrorEvent) -> None:
        """
        Event handler for handling command errors.

        Args:
            event (lightbulb.CommandErrorEvent): The command error event.

        Returns:
            None
        """
        if isinstance(event.exception, lightbulb.CommandInvocationError):
            embed = discord_bot_manager.generate_error_embed("Error!", "Something went wrong!")
            await event.context.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
        if isinstance(event.exception, lightbulb.NotOwner):
            embed = discord_bot_manager.generate_error_embed("Error!", "You aren't the owner of the bot!")
            await event.context.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
        elif isinstance(event.exception, lightbulb.CommandIsOnCooldown):
            m, s = divmod(event.exception.retry_after, 60)
            h, m = divmod(m, 60)
            embed = discord_bot_manager.generate_error_embed(
                "Error!",
                f"You are on cooldown!\nCome back in: {h:.2f} hours, {m:.2f} minutes, {s:.2f} seconds",
            )
            await event.context.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)

    # Run the Bot
    discord_bot_manager.run(status=hikari.Status.IDLE, activity=hikari.Activity(name="I <3 Python", type=hikari.ActivityType.PLAYING))
