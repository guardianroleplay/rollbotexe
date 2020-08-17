# profile_cog.py

from discord.ext import commands
import discord
import re
import sqlite3
import aiosqlite
from rollbot.sql.profile import Profile


class ProfileCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.profile = Profile(bot.sqlite_connection)

    async def get_bot(self):
        return self.bot

    @commands.command(name='add_profile')
    async def add_profile(self, ctx, profile_name: str, *profile_link):
        """Stores a Profile link into the bot"""
        self.profile.set_table_suffix(self.bot.table_suffixes[ctx.guild.id])
        result = await self.profile.add_profile(ctx.author.nick, ctx.author.id, profile_name, ' '.join(profile_link))
        await ctx.send(result)

    @commands.command(name='get_profile')
    async def get_profile(self, ctx, profile_name: str):
        """Gets a Profile link from the bot"""
        self.profile.set_table_suffix(self.bot.table_suffixes[ctx.guild.id])
        result = await self.profile.get_profile(profile_name)
        await ctx.send(result)

    @commands.command(name='del_profile')
    async def del_profile(self, ctx, profile_name: str):
        """Delete a Profile link from the bot, as long as you own it"""
        self.profile.set_table_suffix(self.bot.table_suffixes[ctx.guild.id])
        result = await self.profile.del_profile(ctx.author.id, profile_name)
        await ctx.send(result)


# Add me
def setup(bot):
    bot.add_cog(ProfileCog(bot))
    for suffix in bot.table_suffixes:
        with sqlite3.connect(bot.sqlite_connection) as db:
            db.execute(f'''CREATE TABLE IF NOT EXISTS PROFILE{bot.table_suffixes[suffix]}
                (ID      INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                OWNER    TEXT                              ,
                OWNER_ID INTEGER                           NOT NULL,
                PROFILE  TEXT                              NOT NULL,
                LINK     TEXT                              NOT NULL);''')
