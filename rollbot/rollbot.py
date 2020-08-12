# rollbot.py
import discord
import os

from discord.ext import commands

class RollBot(commands.Bot):
  def __init__(self, *args, **kwargs):
    super(RollBot, self).__init__(*args, **kwargs)

    self.guild_list = kwargs.pop('guild_list', [])
    self.cogs_directory = kwargs.pop('cogs_directory', '')
    self.restricted_permissions = kwargs.pop('restricted_permissions', 0)
    self.cogs_dot_directory = self.cogs_directory.replace('/', '.')

    self.debug = False    
    # load and instantiate any cogs we have
    for filename in os.listdir(self.cogs_directory):
      if filename.endswith('_cog.py'):
        self.load_extension(f'{filename[:-3]}')
    
    # because we rely on the behaviour of discord.py to load cogs,
    # we cannot initialise them using __init__. Instead, we retrieve
    # the cog list, and then run each cog's init()
    #for cog in bot.cogs:
      # do my things with all the cogs here

  def load_extension(self, cog):
    super(RollBot, self).load_extension(f'{self.cogs_dot_directory}{cog}')

  def unload_extension(self, cog):
    super(RollBot, self).unload_extension(f'{self.cogs_dot_directory}{cog}')

  # We don't just bump this up to super, because the super classes' method
  # of reloading does some type introspection that'll cause it to try to 
  # load the wrong module
  def reload_extension(self, cog):
    super(RollBot, self).unload_extension(f'{self.cogs_dot_directory}{cog}')
    super(RollBot, self).load_extension(f'{self.cogs_dot_directory}{cog}')

  async def start(self, *args, **kwargs):
    """
    Login and connect to Discord. The first agument needs to be your dev token
    """
    bot = kwargs.pop('bot', True)
    reconnect = kwargs.pop('reconnect', True)

    if kwargs:
      raise TypeError(f'Unexpected keyword argument(s) {list(kwargs.keys())}')

    await self.login(args[0], bot=bot)
    await self.connect(reconnect=reconnect)

  async def on_ready(self):
    """
    Once connection to Discord is established, this will fire to let us know.
    Note that it may fire more than once if the bot has to reconnect
    """
    print(f'{self.user.name}: {self.user.id} has connected to Discord')
    
    print(f'{self.user.name} is connected to the following servers:')
    for guild in self.guilds:
      status = 'LISTENING' if guild.name in self.guild_list else 'SILENT'
      print(f'- {guild.name}: {status}')

  async def on_command_error(self, ctx, err):
    """
    This catches command errors. The common case of a command not being found is
    handled here, as is the case of someone trying to execute a command without
    proper permissions
    """
    if isinstance(err, commands.CommandNotFound):
      await ctx.send('Command not recognised')
    elif isinstance(err, commands.NotOwner):
      print(f'{ctx.message.author}-{ctx.message.author.id} attempted to use an owner command')
      await ctx.send('Unauthorized')
    else:
      if self.debug:
        await ctx.send(f'**`ERR:`** {type(err).__name__} - {err}')
      else:
        await ctx.send(f'Something went wrong processing your command.')
