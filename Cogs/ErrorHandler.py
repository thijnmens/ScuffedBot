import sys, discord, math, asyncio
from discord.ext import commands

class ErrorHandler(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""

        if hasattr(ctx.command, 'on_error'):
            return
        
        ignored = (commands.UserInputError)
        error = getattr(error, 'original', error)
        
        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.BadArgument):
            print("BadArgument ran")
            return await ctx.send("Bad argument")
        elif isinstance(error, commands.CommandNotFound):
            print("CommandNotFound ran")
            return await ctx.send("S-Sorry Senpai, I couldn't find that command uwu")
        elif isinstance(error, commands.BotMissingPermissions):
            print(f"BotMissingPermissions ran - {error.missing_perms[0]}")
            return await ctx.send(f"Bot missing the following permissions: {error.missing_perms[0]}")
        elif isinstance(error, commands.NotOwner):
                return await ctx.send('Only my owner can do that with me~ >w<')
        elif isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(f"S-Senpai, I'm cooling down! O//w//O\nplease wait {math.ceil(error.retry_after)} seconds uwu")
        elif isinstance(error, commands.CheckFailure) or isinstance(error, commands.MissingPermissions):
            return await ctx.send("Sorry Senpai, you don't have the permissions for this command :(")

    @commands.Cog.listener()
    async def on_ready(self):
        print("ErrorHandler cog loaded")

def setup(client):
    client.add_cog(ErrorHandler(client))
