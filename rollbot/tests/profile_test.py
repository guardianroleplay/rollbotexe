import pytest
import asyncio

from rollbot.cogs.profile_cog import ProfileCog
from unittest.mock import patch, ANY
from rollbot.rollbot import RollBot

class MockDiscord():
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
