# profile.py

import re
import sqlite3
import aiosqlite
import rollbot.profile.profile

class Profile():
    def __init__(self, db):
        self.db = db

    def add_profile(self, author: str, profile_name: str, profile_link: str):
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