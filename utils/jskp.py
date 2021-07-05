from jishaku import Jishaku, Feature
from discord.ext.commands import Context, MissingPermissions

async def cog_check_patch(self: Feature, ctx: Context):
    if "797422816584007720" in str(ctx.author.roles): 
        return True
    raise MissingPermissions("Dev role")


Jishaku.cog_check = cog_check_patch