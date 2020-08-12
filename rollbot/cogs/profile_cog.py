# profile_cog.py

from discord.ext import commands
import discord
import re
import sqlite3
import aiosqlite


class ProfileCog(commands.Cog):

    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    async def getBot(self):
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
                exist_count = await self.db.execute(
                    'SELECT LINK FROM PROFILES WHERE OWNER = ? AND PROFILE = ?',
                    (member, profile_name)
                )
                row = await exist_count.fetchone()
                if (row == None):
                    cursor = await self.db.cursor()
                    await cursor.execute(
                        "INSERT INTO PROFILES (OWNER, PROFILE, LINK) VALUES (?,?,?)",
                        (member, profile_name, profile_link)
                    )
                    await self.db.commit()
                    return await ctx.send(f'** Added "{profile_name}" profile at "{profile_link}"')
                return await ctx.send(f'** Couldn\'t add the profile "{profile_name}", you have already got that profile as {row[0]}')
            else:
                return await ctx.send(f'** Couldn\'t add the profile "{profile_link}", it must be a Discord URL')
        except Exception as ex:
            return await ctx.send(f'{ex}')

    @commands.command(name='get_profile', hidden=True)
    @commands.is_owner()
    async def getProfile(self, ctx, profile_name: str):
        """Get a Profile link from the Database"""
        try:
            results = await self.db.execute(
                'SELECT OWNER, LINK FROM PROFILES WHERE PROFILE = ?',
                (profile_name,)
            )
            to_return = []
            async for row in results:
                to_return.append(f'** {profile_name}({row[0]}): {row[1]}')
            if (len(to_return) == 0):
                return await ctx.send(f'** Could not find a profile for {profile_name}')
            elif (len(to_return) == 1):
                return await ctx.send(f'** {profile_name}: {row[1]}')
            else:
                return await ctx.send('\n'.join(to_return))
        except Exception as ex:
            return await ctx.send(f'**`ERR:`** {type(ex).__name__} - {ex}')

    @commands.command(name='del_profile', hidden=True)
    @commands.is_owner()
    async def delProfile(self, ctx, profile_name: str):
        """Delete a Profile link from the Database"""
        try:
            member = ctx.author
            results = await self.db.execute(
                'SELECT ID, OWNER, LINK FROM PROFILES WHERE PROFILE = ?',
                (profile_name,)
            )
            delete_count = 0
            process_count = 0
            owners = []
            async for row in results:
                process_count += 1
                if (row[1] == member):
                    cursor = await self.db.cursor()
                    await cursor.execute(
                        "DELETE FROM PROFILES WHERE ID = ?",
                        (row[0],)
                    )
                    await self.db.commit()
                    delete_count += 1
                else:
                    owners.append(row[1])

            if (process_count == 0):
                return await ctx.send(f'** Could not find a profile for {profile_name}')
            elif (delete_count == 0):
                owners_string = ','.join(owners)
                return await ctx.send(f'** You do not own {profile_name}({owners_string})')
            elif (process_count > 1):
                return await ctx.send(f'** Deleted {profile_name}({member})')
            else:
                return await ctx.send(f'** Deleted {profile_name}')
                

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
