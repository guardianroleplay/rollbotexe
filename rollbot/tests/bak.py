import pytest
import asyncio
import sqlite3
import aiosqlite

from unittest.mock import patch, ANY
from pymongo import MongoClient
import rollbot.cogs.profile_cog

# DISCORD MOCK


class MockDiscord():

    def __init__(self):
        self.author = "Owner#1"

    async def send(self, x: str):
        return x


disc = MockDiscord()

# SQL MOCK
async def create_mock_db():
    async with aiosqlite.connect(':memory:') as db:
        await db.execute('''CREATE TABLE PROFILES
                (ID      INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                OWNER    CHAR(50)                          NOT NULL,
                PROFILE  CHAR(50)                          NOT NULL,
                LINK     CHAR(255)                         NOT NULL);''')
        await db.execute("INSERT INTO PROFILES (ID,OWNER,PROFILE,LINK) VALUES (1, 'Sethur#234', 'Sethur', 'https://discordapp.com/Seth')")
        await db.execute("INSERT INTO PROFILES (ID,OWNER,PROFILE,LINK) VALUES (2, 'Owner#1', 'MultipleMan', 'https://xxx')")
        await db.execute("INSERT INTO PROFILES (ID,OWNER,PROFILE,LINK) VALUES (3, 'Owner#2', 'MultipleMan', 'https://xxx')")
        await db.execute("INSERT INTO PROFILES (ID,OWNER,PROFILE,LINK) VALUES (4, 'Owner#2', 'Curly', 'https://xxx')")
        await db.execute("INSERT INTO PROFILES (ID,OWNER,PROFILE,LINK) VALUES (5, 'Owner#1', 'Larry', 'https://xxx')")
        await db.execute("INSERT INTO PROFILES (ID,OWNER,PROFILE,LINK) VALUES (6, 'Owner#2', 'Larry', 'https://xxx')")
        await db.execute("INSERT INTO PROFILES (ID,OWNER,PROFILE,LINK) VALUES (7, 'Owner#1', 'Moe', 'https://xxx')")
    return await db

def test_bot():
    profile = ProfileCog(None, create_mock_db())
    assert None == profile.getBot()


@pytest.mark.asyncio
async def test_profile_help():
    profile = ProfileCog(None, create_mock_db())
    returned_post = await profile.helpProfile(profile, disc)
    assert returned_post == '** add_profile <name> <link> to add a link to a profile\n** del_profile <name> to remove the link to a profile\n**profile <name> to find a profile by name\n** To get the link to your profile, hover over the post, click the ... and Copy MessageLink'


@pytest.mark.asyncio
async def test_profile_add():
    profile = ProfileCog(None, create_mock_db())

    add_result = await profile.addProfile(profile, disc, 'Relapse', 'https://google.com/channels/735710358333030460/735881650311004160/742695586133966898')
    assert add_result == '** Couldn\'t add the profile "https://google.com/channels/735710358333030460/735881650311004160/742695586133966898", it must be a Discord URL'

    add_result = await profile.addProfile(profile, disc, 'Relapse', 'https://discordapp.com/channels/735710358333030460/735881650311004160/742695586133966898')
    assert add_result == '** Added "Relapse" profile at "https://discordapp.com/channels/735710358333030460/735881650311004160/742695586133966898"'

    add_result = await profile.addProfile(profile, disc, 'Relapse', 'https://discordapp.com/channels/735710358333030461/735881650311004160/742695586133966891')
    assert add_result == '** Couldn\'t add the profile "Relapse", you have already got that profile as https://discordapp.com/channels/735710358333030460/735881650311004160/742695586133966898'


@pytest.mark.asyncio
async def test_profile_get():
    profile = ProfileCog(None, create_mock_db())

    get_result = await profile.getProfile(profile, disc, 'Sethur')
    assert get_result == '** Sethur: https://discordapp.com/Seth'

    get_result = await profile.getProfile(profile, disc, 'Tellana')
    assert get_result == '** Could not find a profile for Tellana'

    get_result = await profile.getProfile(profile, disc, 'MultipleMan')
    assert get_result == '** MultipleMan(Owner#1): https://xxx\n** MultipleMan(Owner#2): https://xxx'


@pytest.mark.asyncio
async def test_profile_del():
    profile = ProfileCog(None, create_mock_db())

    del_result = await profile.delProfile(profile, disc, 'Zeppo')
    assert del_result == '** Could not find a profile for Zeppo'

    del_result = await profile.delProfile(profile, disc, 'Curly')
    assert del_result == '** You do not own Curly(Owner#2)'

    del_result = await profile.delProfile(profile, disc, 'Larry')
    assert del_result == '** Deleted Larry(Owner#1)'

    del_result = await profile.delProfile(profile, disc, 'Moe')
    assert del_result == '** Deleted Moe'

    del_result = await profile.delProfile(profile, disc, 'Larry')
    assert del_result == '** You do not own Larry(Owner#2)'