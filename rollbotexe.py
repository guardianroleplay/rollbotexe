#!/usr/bin/python3
import os
from dotenv import load_dotenv

from discord.ext import commands

from rollbot.rollbot import RollBot
from rollbot.profile.profile import Profile

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
    TABLE_SUFFIX = os.getenv('TABLE_SUFFIX')
    SQLITE_CONNECTION = os.getenv('SQLITE_CONNECTION')

    return RollBot(command_prefix='!', description='RollBot.EXE', guild_list=GUILDS, cogs_directory='rollbot/cogs/', restricted_permissions=RESTRICTED_PERMISSIONS, table_suffix=TABLE_SUFFIX, profile=Profile(SQLITE_CONNECTION, TABLE_SUFFIX)), TOKEN

if __name__ == '__main__':
    bot, token = load_bot()
    bot.run(token)
