import sys, discord, math, asyncio, logging
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
            logging.info("BadArgument ran")
            return await ctx.send("Bad argument")
        elif isinstance(error, commands.CommandNotFound):
            logging.info("CommandNotFound ran")
            return await ctx.send("Command not found")
        elif isinstance(error, commands.BotMissingPermissions):
            logging.info(f"BotMissingPermissions ran - {error.missing_perms[0]}")
            return await ctx.send(f"Bot missing the following permissions: {error.missing_perms[0]}")
        elif isinstance(error, commands.NotOwner):
                return await ctx.send('Only the bot owner can run this command')
        elif isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(f"Command on cooldown, wait {math.ceil(error.retry_after)} seconds")
        elif isinstance(error, commands.CheckFailure) or isinstance(error, commands.MissingPermissions):
            return await ctx.send("You don't have the valid permissions for this command")

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("ErrorHandler cog loaded")

def setup(client):
    client.add_cog(ErrorHandler(client))
