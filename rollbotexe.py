#!/usr/bin/python3
import ast
import os
from dotenv import load_dotenv

from discord.ext import commands

from rollbot.rollbot import RollBot


def try_parse_int(string, base=10, val=None):
    try:
        return int(string, base)
    except ValueError:
        return val


def load_bot():
    load_dotenv()

    TOKEN = os.getenv('DISCORD_TOKEN')
    GUILDS = os.getenv('DISCORD_GUILDS').split(',')
    RESTRICTED_PERMISSIONS = try_parse_int(
        os.getenv('RESTRICTED_PERMISSIONS'), 10, 8)
    TABLE_SUFFIXES = ast.literal_eval(os.getenv('TABLE_SUFFIX'))
    SQLITE_CONNECTION = os.getenv('SQLITE_CONNECTION')

    return RollBot(command_prefix='!', description='RollBot.EXE', guild_list=GUILDS, cogs_directory='rollbot/cogs/', restricted_permissions=RESTRICTED_PERMISSIONS, table_suffixes=TABLE_SUFFIXES, sqlite_connection=SQLITE_CONNECTION), TOKEN


if __name__ == '__main__':
    bot, token = load_bot()
    bot.run(token)
