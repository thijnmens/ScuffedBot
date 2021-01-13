import sys, discord, math, asyncio
from discord.ext import commands

class ErrorHandler(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print (f"on_command_error triggered")
        if isinstance(error, commands.BadArgument):
            print("BadArgument handler ran")
            return await ctx.send("Bad argument") #ngl I have no clue when this error is invoked but whatever

        elif isinstance(error, commands.CommandNotFound):
            print("CommandNotFound handler ran")
            return await ctx.send("S-Sorry Senpai, I couldn't find that command qwq")

        elif isinstance(error, commands.BotMissingPermissions):
            print(f"BotMissingPermissions handler ran - {error.missing_perms[0]}")
            return await ctx.send(f"Bot missing the following permissions: {error.missing_perms[0]}")

        elif isinstance(error, commands.NotOwner):
            print ("NotOwner handler ran")
            return await ctx.send('Only my owner can do that with me~ >w<')

        elif isinstance(error, commands.CommandOnCooldown):
            print ("CommandOnCooldown handler ran")
            return await ctx.send(f"S-Senpai, I'm cooling down! O//w//O\nplease wait {math.ceil(error.retry_after)} seconds uwu")

        elif isinstance(error, commands.MissingRequiredArgument):
            print ("MissingRequiredArgument handler ran")
            return await ctx.send(f"You didn't give a required argument, B-Baka!")#\n``Missing: {error.param.name}``")

        elif isinstance(error, commands.CheckFailure) or isinstance(error, commands.MissingPermissions):
            print ("MissingPermissions handler ran")
            return await ctx.send("Sorry Senpai, you don't have the permissions for this command qwq")
        print (error)
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("ErrorHandler cog loaded")

def setup(client):
    client.add_cog(ErrorHandler(client))
