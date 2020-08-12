# role_cog.py
from discord.ext import commands
from discord.utils import get
import discord

class RoleCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  def allowed_role(self, role):
    """
    Check to see if a role is allowed to be assigned by the bot by comparing the role's
    permissions against the forbidden permissions list
    """
    restricted_permissions = discord.Permissions(self.bot.restricted_permissions)
    
    for role in role.permissions:
      forbidden = role[1] and restricted_permissions.__getattribute__(role[0])
      if forbidden:
        return False
    return True

  @commands.command()
  async def check_role(self, ctx, *, requested_role: str):
    """Check a role to see if the bot will assign it to you"""
    role = get(ctx.guild.roles, name=requested_role)
    if role is None:
      await ctx.send(f'Role {requested_role} does not seem to exist')
      return

    if self.allowed_role(role):
      await ctx.send('You may ask for that role')
    else:
      await ctx.send('You will need to ask Staff for that role')    

  @commands.command()
  async def role(self, ctx, *, requested_role: str):
    """Add a role to yourself, or, if you already have it, remove a role from yourself. Usage: !role role_name"""
    member = ctx.author
    role = get(ctx.guild.roles, name=requested_role)

    if role is None:
      await ctx.send(f'Role {requested_role} does not seem to exist, and thus, I cannot assign it')
      return
    if not self.allowed_role(role):
      await ctx.send(f'I cannot assign {role.name}.')
      return

    if role in member.roles:
      await member.remove_roles(role)
      await ctx.send(f'Removed {role.name} from {member.display_name}')
    else:
      await member.add_roles(role)
      await ctx.send(f'Added {role.name} to {member.display_name}')

  @commands.command()
  async def role_list(self, ctx, *, debug: str = ''):
    """Get a list of all the roles available on the server."""
    roles = await ctx.guild.fetch_roles()

    role_list = 'Roles:'
    if self.bot.debug:
      for role in (role for role in roles if not role.is_default()):
        role_list += f'\n {role.name} - {role.id}'
    else:
      for role in (role for role in roles if not role.is_default()):
        role_list += f'\n {role.name}'
    await ctx.send(f'{role_list}')

def setup(bot):
  bot.add_cog(RoleCog(bot))