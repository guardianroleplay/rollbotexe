# basic_cog.py
from discord.ext import commands
import discord

class BasicCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  # This is an example of a Cog-level listener. Consider putting this kind of thing in RollBot instead.
  @commands.Cog.listener()
  async def on_member_join(self, member):
    channel = member.guild.system_channel
    if channel is not None:
      await channel.send(f'Welcome {member.mention}')
    
  @commands.command()
  async def hello(self, ctx, *, member: discord.Member = None):
    """Greets the user"""
    # pylint: disable=anomalous-backslash-in-string
    await ctx.send(f'Hi there \o^_^o/')

def setup(bot):
  bot.add_cog(BasicCog(bot))