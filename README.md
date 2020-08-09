# RollBotExe

A Discord Bot

## About

RollBotEXE uses the Discord Python library to interface with Discord servers. Documentation for that library is available [here](https://discordpy.readthedocs.io/en/latest/)

## I'm a user! Tell me about bot commands.

Commands universally begin with a !, and you can get a list of them from RollBotEXE itself by typing !help in a channel the bot is in.

## Developers
### Pre-requisites

If you're coming from the Guardians server, welcome! Glad to have you. The RollBotEXE running there is running under biot8's user account.

If you want to run this bot on your local machine, you will need to run it under your own account. I recommend making your own server as well
to experiment in.

To do this, you will need to establish a developer account. The discord.py documentation has instructions for that [here](https://discordpy.readthedocs.io/en/latest/discord.html).
All of the steps are important, but take special care to pay attention to step 7; take note of your token, as you'll need it for the bot to get online.

### Running the bot

You will need Python 3 (version 3.8 or greater) and Pip working

To download the Discord library, run:

~~~
pip install -U discord.py
~~~

The token you acquired in the pre-requisites section is important here.
You will need to make an new file named .env in the same directory as main.py. The .env file expects to be formatted like so (do not include the curly brackets):

~~~
# .env
DISCORD_TOKEN={token string from Discord OAuth}
DISCORD_GUILDS={Comma-seperated list of servers the bot will pay attention to}
RESTRICTED_PERMISSIONS={Permissions integer of permissions bot will not assign to people; can be generated at Discord's developer portal}
~~~

After that, you should be able to just run the main python script.

### Contribution

If you wish to add commands to the bot, look at basic_cog.py for a bare-bones simple example of what a cognition looks like.
Please group your commands by cognition.
All cogs must go in the cogs folder, and end in _cog.py
We generally follow the guidlines of PEP 8 for formatting and naming
Prefer f-strings for formatted string duties
Checking in directly into master is not permitted; you will need to create a branch, and then publish the branch to GitHub, and then create a pull request for your changes.

Bot redeploys on an irregular schedule