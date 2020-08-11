import pytest
import asyncio

from rollbot.cogs.profile_cog import ProfileCog
from unittest.mock import patch, ANY
from rollbot.rollbot import RollBot
from pymongo import MongoClient

# DISCORD MOCK


class MockDiscord():

    def __init__(self):
        self.author = "Owner#1"

    async def send(self, x: str):
        return x


disc = MockDiscord()

# SQL MOCK
class MockDatabase():
    def __init__(self):
        self.profiles = [
            {
                'Owner': 'Sethur#234',
                'Profile': 'Sethur',
                'Link': 'https://discordapp.com/Seth'
            }, {
                'Owner': 'Owner#1',
                'Profile': 'MultipleMan',
                'Link': 'https://xxx'
            }, {
                'Owner': 'Owner#2',
                'Profile': 'MultipleMan',
                'Link': 'https://xxx'
            }, {
                'Owner': 'Owner#2',
                'Profile': 'Curly',
                'Link': 'https://xxx'
            }, {
                'Owner': 'Owner#1',
                'Profile': 'Larry',
                'Link': 'https://xxx'
            }, {
                'Owner': 'Owner#2',
                'Profile': 'Larry',
                'Link': 'https://xxx'
            }, {
                'Owner': 'Owner#1',
                'Profile': 'Moe',
                'Link': 'https://xxx'
            }
        ]

    def insert_one(self, x: dict):
        self.profiles.append(x)

    def delete_one(self, owner: str, name:str):
        for idx, val in enumerate(self.profiles):
            if (val['Owner'] == owner and val['Profile'] == name):
                self.profiles.pop(idx)

    def find_one(self, name: str):
        to_return = []
        for x in self.profiles:
            if (x['Profile'] == name):
                to_return.append(x)
        return to_return

db = MockDatabase()

def test_bot():
    profile = ProfileCog(None, db)
    assert None == profile.getBot()


@pytest.mark.asyncio
async def test_profile_help():
    profile = ProfileCog(None, db)
    returned_post = await profile.helpProfile(profile, disc)
    assert returned_post == '** add_profile <name> <link> to add a link to a profile\n** del_profile <name> to remove the link to a profile\n**profile <name> to find a profile by name\n** To get the link to your profile, hover over the post, click the ... and Copy MessageLink'


@pytest.mark.asyncio
async def test_profile_add():
    profile = ProfileCog(None, db)

    add_result = await profile.addProfile(profile, disc, 'Relapse', 'https://google.com/channels/735710358333030460/735881650311004160/742695586133966898')
    assert add_result == '** Couldn\'t add the profile "https://google.com/channels/735710358333030460/735881650311004160/742695586133966898", it must be a Discord URL'

    add_result = await profile.addProfile(profile, disc, 'Relapse', 'https://discordapp.com/channels/735710358333030460/735881650311004160/742695586133966898')
    assert add_result == '** Added "Relapse" profile at "https://discordapp.com/channels/735710358333030460/735881650311004160/742695586133966898"'


@pytest.mark.asyncio
async def test_profile_get():
    profile = ProfileCog(None, db)

    get_result = await profile.getProfile(profile, disc, 'Sethur')
    assert get_result == '** Sethur: https://discordapp.com/Seth'

    get_result = await profile.getProfile(profile, disc, 'Tellana')
    assert get_result == '** Could not find a profile for Tellana'

    get_result = await profile.getProfile(profile, disc, 'MultipleMan')
    assert get_result == '** MultipleMan(Owner#1): https://xxx\n** MultipleMan(Owner#2): https://xxx'


@pytest.mark.asyncio
async def test_profile_del():
    profile = ProfileCog(None, db)

    del_result = await profile.delProfile(profile, disc, 'Zeppo')
    assert del_result == '** Could not find a profile for Zeppo'

    del_result = await profile.delProfile(profile, disc, 'Curly')
    assert del_result == '** You do not own Curly(Owner#2)'

    del_result = await profile.delProfile(profile, disc, 'Larry')
    assert del_result == '** Deleted Larry(Owner#1)'

    del_result = await profile.delProfile(profile, disc, 'Moe')
    assert del_result == '** Deleted Moe'
