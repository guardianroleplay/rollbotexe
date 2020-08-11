import pytest
import asyncio

from rollbot.cogs.profile_cog import ProfileCog
from unittest.mock import patch, ANY
from rollbot.rollbot import RollBot

class MockDiscord():

    def __init__(self):
        self.author = "Colin#12321"

    async def send(self, x: str):
        return x

disc = MockDiscord()

def test_bot():
    profile = ProfileCog(None)
    assert None == profile.getBot()

@pytest.mark.asyncio
async def test_profile_help():
    profile = ProfileCog(None)
    returned_post = await profile.helpProfile(profile, disc)
    assert returned_post == '** add_profile <name> <link> to add a link to a profile\n** del_profile <name> to remove the link to a profile\n**profile <name> to find a profile by name\n** To get the link to your profile, hover over the post, click the ... and Copy MessageLink'

@pytest.mark.asyncio
async def test_profile_add():
    profile = ProfileCog(None)

    add_result = await profile.addProfile(profile, disc, 'Relapse', 'https://google.com/channels/735710358333030460/735881650311004160/742695586133966898')
    assert add_result == '** Couldn\'t add the profile "https://google.com/channels/735710358333030460/735881650311004160/742695586133966898", it must be a Discord URL'

    add_result = await profile.addProfile(profile, disc, 'Relapse', 'https://discordapp.com/channels/735710358333030460/735881650311004160/742695586133966898')
    assert add_result == '** Added "Relapse" profile at "https://discordapp.com/channels/735710358333030460/735881650311004160/742695586133966898"'

@pytest.mark.asyncio
async def test_profile_get():
    profile = ProfileCog(None)

    get_result = await profile.getProfile(profile, disc, 'Sethur')
    assert get_result == '** Sethur: https://xxx'

    get_result = await profile.getProfile(profile, disc, 'Tellana')
    assert get_result == '** Could not find a profile for Tellana'

    get_result = await profile.getProfile(profile, disc, 'MultipleMan')
    assert get_result == '** MultipleMan(Owner#1): https://xxx\n** MultipleMan(Owner#2): https://xxx'

@pytest.mark.asyncio
async def test_profile_del():
    profile = ProfileCog(None)

    del_result = await profile.delProfile(profile, disc, 'Curly')
    assert del_result == '** You do not own Curly(Owner#2)'

    del_result = await profile.delProfile(profile, disc, 'Larry')
    assert del_result == '** Deleted Larry(Owner#1)'

    del_result = await profile.delProfile(profile, disc, 'Moe')
    assert del_result == '** Deleted Moe'

# class ProfileTestCase(unittest.TestCase):
# 
#     def test_initialization(self):
#         profile = ProfileCog(None)
#         self.assertEqual(profile.getBot(), None)
# 
# #    def test_add(self):
# #
# #    def test_delete(self):
# #
# #    def test_find(self):
#     
#     async def test_help(self):
#         profile = ProfileCog(None)
#         try:
#             x = await profile.helpProfile(MockDiscord())
#             self.assertEqual(True, x)
#         except Exception as ex:
#             self.fail(f'**`ERR:`** {type(ex).__name__} - {ex}')
