# profile_cog.py

from discord.ext import commands
import discord
import re
import sqlite3
import aiosqlite

class ProfileCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.profile = bot.profile

    async def get_bot(self):
        return self.bot

    @commands.command(name='add_profile', hidden=True)
    @commands.is_owner()
    async def add_profile(self, ctx, profile_name: str, profile_link: str):
        """Stores a Profile link into the Database"""
        try:
            result = await self.profile.add_profile(ctx.author.nick, ctx.author.id, profile_name, profile_link)
            await ctx.send(result)
        except Exception as ex:
            await ctx.send(f'{ex}')

    @commands.command(name='get_profile', hidden=True)
    @commands.is_owner()
    async def get_profile(self, ctx, profile_name: str):
        """Get a Profile link from the Database"""
        try:
            result = await self.profile.get_profile(profile_name)
            await ctx.send(result)
        except Exception as ex:
            await ctx.send(f'**`ERR:`** {type(ex).__name__} - {ex}')

    @commands.command(name='del_profile', hidden=True)
    @commands.is_owner()
    async def del_profile(self, ctx, profile_name: str):
        """Delete a Profile link from the Database"""
        try:
            result = await self.profile.del_profile(ctx.author.id, profile_name)
            await ctx.send(result)
        except Exception as ex:
            await ctx.send(f'**`ERR:`** {type(ex).__name__} - {ex}')

    @commands.command(name='help_profile', hidden=True)
    @commands.is_owner()
    async def help_profile(self, ctx):
        """ Prompts how this works"""
        try:
            await ctx.send('```\n* add_profile <name> <link> to add a link to a profile\n* del_profile <name> to remove the link to a profile\n* get_profile <name> to find a profile by name\n\nTo get the link to your profile:\n* hover over the post\n* click the ...\n* copy MessageLink```')
        except Exception as ex:
            await ctx.send(f'**`ERR:`** {type(ex).__name__} - {ex}')


# Add me
def setup(bot):
    bot.add_cog(ProfileCog(bot))
