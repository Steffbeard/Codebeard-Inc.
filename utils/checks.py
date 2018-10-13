from discord.ext import commands
import discord.utils

#
# This is a modified version of checks.py, originally made by Rapptz
#
#                 https://github.com/Rapptz
#          https://github.com/Rapptz/RoboDanny/tree/async
#
# 411955563954569226 is ignatius
# 438345376320192514 is blake
# 178653059096772611 is steffbeard
# 489211942603456512 is the server ID (bg)
# 499019897754484737 is the server ID (test)
#

def is_owner(ctx):
    return ctx.author.id == 178653059096772611 or ctx.author.id == 411955563954569226 or ctx.author.id == 298421225280110592

def is_admin(ctx):
    role = discord.utils.get(ctx.bot.get_guild(489211942603456512).roles, name='Staff')
    user = discord.utils.get(ctx.bot.get_guild(489211942603456512).members, id=ctx.author.id)
    return role in user.roles or is_owner(ctx)

def check_permissions(ctx, perms):
    if is_owner(ctx):
        return True
    elif not perms:
        return False

    ch = ctx.message.channel
    author = ctx.author
    resolved = ch.permissions_for(author)
    return all(getattr(resolved, name, None) == value for name, value in perms.items())

def role_or_permissions(ctx, check, **perms):
    if check_permissions(ctx, perms):
        return True

    ch = ctx.message.channel
    author = ctx.author
    if ch.is_private:
        return False # can't have roles in PMs

    role = discord.utils.find(check, author.roles)
    return role is not None

def serverowner_or_permissions(**perms):
    def predicate(ctx):
        if ctx.message.guild is None:
            return False
        server = ctx.message.guild
        owner = server.owner

        if ctx.author.id == owner.id:
            return True

        return check_permissions(ctx,perms)
    return commands.check(predicate)

def serverowner():
    return serverowner_or_permissions()
