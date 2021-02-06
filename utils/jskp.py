from jishaku import Jishaku, JishakuBase
from discord.ext.commands import Context

async def cog_check_patch(self: JishakuBase, ctx: Context):
    print("Jishaku check")
    print (ctx.author.roles)
    if "797422816584007720" in str(ctx.author.roles): 
        print ("true")
        return True
    print ("false")
    return False

Jishaku.cog_check = cog_check_patch