# profile_cog.py

from discord.ext import commands
import discord
import re
import sqlite3
import aiosqlite
from rollbot.profile.profile import Profile

class ProfileCog(commands.Cog):

    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
        self.profile = Profile(db)

    async def getBot(self):
        return self.bot

    @commands.command(name='add_profile', hidden=True)
    @commands.is_owner()
    async def addProfile(self, ctx, profile_name: str, profile_link: str):
        """Stores a Profile link into the Database"""
        try:
            result = await self.profile.add_profile(ctx.author, profile_name, profile_link)
            return await ctx.send(result)
        except Exception as ex:
            return await ctx.send(f'{ex}')

    @commands.command(name='get_profile', hidden=True)
    @commands.is_owner()
    async def getProfile(self, ctx, profile_name: str):
        """Get a Profile link from the Database"""
        try:
            result = await self.profile.get_profile(profile_name)
            return await ctx.send(result)
        except Exception as ex:
            return await ctx.send(f'**`ERR:`** {type(ex).__name__} - {ex}')

    @commands.command(name='del_profile', hidden=True)
    @commands.is_owner()
    async def delProfile(self, ctx, profile_name: str):
        """Delete a Profile link from the Database"""
        try:
            result = await self.profile.del_profile(ctx.author, profile_name)
            return await ctx.send(result)
        except Exception as ex:
            await ctx.send(f'**`ERR:`** {type(ex).__name__} - {ex}')

    @commands.command(name='help_profile', hidden=True)
    @commands.is_owner()
    async def helpProfile(self, ctx):
        """ Prompts how this works"""
        try:
            return await ctx.send('** add_profile <name> <link> to add a link to a profile\n** del_profile <name> to remove the link to a profile\n**profile <name> to find a profile by name\n** To get the link to your profile, hover over the post, click the ... and Copy MessageLink')
        except Exception as ex:
            await ctx.send(f'**`ERR:`** {type(ex).__name__} - {ex}')


# Add me
def setup(bot):
    bot.add_cog(ProfileCog(bot))
