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
    try:
      self.bot.load_extension(cog)
    except Exception as ex:
      await ctx.send(f'**`ERR:`** {type(ex).__name__} - {ex}')
    else:
      await ctx.send(f'**`Successfully loaded {cog}`**')

  @commands.command(name='unload', hidden=True)
  @commands.is_owner()
  async def dev_unload(self, ctx, *, cog: str):
    """Unload an already loaded cog. Full dot path required (ex: cogs.roll_cog)"""
    try:
      self.bot.unload_extension(cog)
    except Exception as ex:
      await ctx.send(f'**`ERR:`** {type(ex).__name__} - {ex}')
    else:
      await ctx.send(f'**`Successfully unloaded {cog}`**')

  @commands.command(name='reload', hidden=True)
  @commands.is_owner()
  async def dev_reload(self, ctx, *, cog: str):
    """Reload cog. Full dot path required (ex: cogs.roll_cog)"""
    try:
      self.bot.reload_extension(cog)
    except Exception as ex:
      await ctx.send(f'**`ERR:`** {type(ex).__name__} - {ex}')
    else:
      await ctx.send(f'**`{cog} successfully reloaded!`**')

def setup(bot):
  bot.add_cog(DevCog(bot))