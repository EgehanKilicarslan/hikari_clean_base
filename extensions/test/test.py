# Created by Egehan Kılıçarslan on 31/12/2023
# This file is part of a project developed by Egehan Kılıçarslan.

import hikari
import lightbulb
import sys

sys.path.insert(1, "./")

from utils.utils import Config, MongoDBManager, generate_secret
from typing import Any

plugin = lightbulb.Plugin("test")

SUCCESS_COLOR = Config().SUCCESS_COLOR
ERROR_COLOR = Config().ERROR_COLOR


@plugin.command()
@lightbulb.command("test", "This is a test command.")
@lightbulb.implements(lightbulb.SlashCommand)
async def test(ctx: lightbulb.ApplicationContext) -> None:
    error_messages = {
        "This command is not available in this server!": ctx.guild_id != Config().SERVERS[0]
    }

    for message, condition in error_messages.items():
        if condition:
            embed = hikari.Embed(title="Error!", description=message, color=ERROR_COLOR)
            break
    else:
        embed = hikari.Embed(
            title="Success!",
            description="This is a test command",
            color=SUCCESS_COLOR,
        )

    await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)


def load(bot: Any) -> None:
    bot.add_plugin(plugin)
