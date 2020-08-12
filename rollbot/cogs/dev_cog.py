# dev_cog.py
from discord.ext import commands
import discord

class DevCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name='load', hidden=True)
  @commands.is_owner()
  async def dev_load(self, ctx, *, cog: str):
    """Load cog. Full dot path required (ex: cogs.roll_cog)"""
    self.bot.load_extension(cog)
    await ctx.send(f'**`Successfully loaded {cog}`**')

  @commands.command(name='unload', hidden=True)
  @commands.is_owner()
  async def dev_unload(self, ctx, *, cog: str):
    """Unload an already loaded cog. Full dot path required (ex: cogs.roll_cog)"""
    self.bot.unload_extension(cog)
    await ctx.send(f'**`Successfully unloaded {cog}`**')

  @commands.command(name='reload', hidden=True)
  @commands.is_owner()
  async def dev_reload(self, ctx, *, cog: str):
    """Reload cog. Full dot path required (ex: cogs.roll_cog)"""
    self.bot.reload_extension(cog)
    await ctx.send(f'**`{cog} successfully reloaded!`**')

  @commands.command(name='debug', hidden=True)
  @commands.is_owner()
  async def dev_debug(self, ctx):
    """Toggle debug mode. Debug mode will display IDs and put error messages in chat"""
    self.bot.debug = not self.bot.debug
    debug_mode = 'ON' if self.bot.debug else 'OFF'
    await ctx.send(f'Debug mode: {debug_mode}')

  @commands.command(name='server_list', hidden=True)
  @commands.is_owner()
  async def dev_servers(self, ctx):
    """List of servers the bot is connected to. In debug mode, also provides their IDs"""
    servers = 'Servers I am connected to:'
    if self.bot.debug:
      for guild in self.bot.guilds:
        servers += f'\n{guild.name} - {guild.id}'
    else:
      for guild in self.bot.guilds:
        servers += f'\n{guild.name}'
    await ctx.send(servers)
  
  @commands.command(name='leave_server', hidden=True)
  @commands.is_owner()
  async def dev_leave(self, ctx, *, server_id: str):
    """Tells the bot to exit a server. Provide server ID, not server name"""
    server_to_leave = self.bot.get_guild(int(server_id, 10))
    await server_to_leave.leave()

def setup(bot):
  bot.add_cog(DevCog(bot))