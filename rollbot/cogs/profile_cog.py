# profile_cog.py

from discord.ext import commands
import discord
import re


class ProfileCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def getBot(self):
        return self.bot

    @commands.command(name='add_profile', hidden=True)
    @commands.is_owner()
    async def addProfile(self, ctx, profile_name: str, profile_link: str):
        """Stores a Profile link into the Database"""
        try:
            regex = re.compile(
                r'^https://discordapp.com/channels/\d{18}/\d{18}/\d{18}',
                re.IGNORECASE
            )
            if (re.match(regex, profile_link) is not None):
                member = ctx.author
                # Do the save thing
                return await ctx.send(f'** Added "{profile_name}" profile at "{profile_link}"')
            else:
                return await ctx.send(f'** Couldn\'t add the profile "{profile_link}", it must be a Discord URL')
        except Exception as ex:
            await ctx.send(f'**`ERR:`** {type(ex).__name__} - {ex}')

    @commands.command(name='get_profile', hidden=True)
    @commands.is_owner()
    async def getProfile(self, ctx, profile_name: str):
        """Get a Profile link from the Database"""
        try:
            # Get the ProfileName from the database
            # If its None, then we cannae do it
            # If it's not None, but one, show single
            # If it's not None, but multiple, show multiple
            profile_link = 'Mock'
            return await ctx.send(f'** {profile_name}: "{profile_link}", it must be a Discord URL')
        except Exception as ex:
            await ctx.send(f'**`ERR:`** {type(ex).__name__} - {ex}')

    @commands.command(name='del_profile', hidden=True)
    @commands.is_owner()
    async def delProfile(self, ctx, profile_name: str):
        """Delete a Profile link from the Database"""
        try:
            member = ctx.author
            
            # Get the ProfileName from the database, owned by member
            # If its None, then we cannae do it
            # If it is not None, then we can delete it
            return await ctx.send(f'** Deleted {profile_name} for you')
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
