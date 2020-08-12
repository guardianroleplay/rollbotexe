# profile.py

import re
import sqlite3
import aiosqlite
import rollbot.profile.profile

class Profile():
    def __init__(self, db):
        self.db = db

    async def add_profile(self, member: str, profile_name: str, profile_link: str):
        regex = re.compile(
            r'^https://discordapp.com/channels/\d{18}/\d{18}/\d{18}',
            re.IGNORECASE
        )

        if (re.match(regex, profile_link) is not None):
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
                return f'** Added "{profile_name}" profile at "{profile_link}"'
            return f'** Couldn\'t add the profile "{profile_name}", you have already got that profile as {row[0]}'
        else:
            return f'** Couldn\'t add the profile "{profile_link}", it must be a Discord URL'

    async def get_profile(self, profile_name: str):
        results = await self.db.execute(
            'SELECT OWNER, LINK FROM PROFILES WHERE PROFILE = ?',
            (profile_name,)
        )
        to_return = []
        async for row in results:
            to_return.append(f'** {profile_name}({row[0]}): {row[1]}')
        if (len(to_return) == 0):
            return f'** Could not find a profile for {profile_name}'
        elif (len(to_return) == 1):
            return f'** {profile_name}: {row[1]}'
        else:
            return '\n'.join(to_return)

    async def del_profile(self, member: str, profile_name: str):
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

        await results.close()
        if (process_count == 0):
            return f'** Could not find a profile for {profile_name}'
        elif (delete_count == 0):
            owners_string = ','.join(owners)
            return f'** You do not own {profile_name}({owners_string})'
        elif (process_count > 1):
            return f'** Deleted {profile_name}({member})'
        else:
            return f'** Deleted {profile_name}'