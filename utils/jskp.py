from jishaku import Jishaku, JishakuBase
from discord.ext.commands import Context

async def cog_check_patch(self: JishakuBase, ctx: Context):
    print("Jishaku check")
    if "797422816584007720" in ctx.author.roles: 
        return True
    return False

Jishaku.cog_check = cog_check_patch