import sys
import discord
import math
import asyncio
import logging
from discord.ext import commands


class error_handler(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        logging.info(f"on_command_error triggered")
        if isinstance(error, commands.BadArgument):
            logging.info("BadArgument handler ran")
            # ngl I have no clue when this error is invoked but whatever
            return await ctx.send("Bad argument")

        elif isinstance(error, commands.CommandNotFound):
            logging.info("CommandNotFound handler ran")
            return await ctx.send("S-Sorry Senpai, I couldn't find that command qwq", delete_after=20)

        elif isinstance(error, commands.BotMissingPermissions):
            logging.info(f"BotMissingPermissions handler ran - {error.missing_perms[0]}")
            return await ctx.send(f"Bot missing the following permissions: {error.missing_perms[0]}")

        elif isinstance(error, commands.NotOwner):
            logging.info("NotOwner handler ran")
            return await ctx.send('Only my owner can do that with me~ >w<')

        elif isinstance(error, commands.CommandOnCooldown):
            logging.info("CommandOnCooldown handler ran")
            return await ctx.send(f"S-Senpai, I'm cooling down! O//w//O\nplease wait {math.ceil(error.retry_after)} seconds uwu")

        elif isinstance(error, commands.MissingRequiredArgument):
            logging.info("MissingRequiredArgument handler ran")
            # \n``Missing: {error.param.name}``")
            return await ctx.send(f"You didn't give a required argument, B-Baka!")

        elif isinstance(error, commands.CheckFailure) or isinstance(error, commands.MissingPermissions):
            logging.info("MissingPermissions handler ran")
            return await ctx.send("Sorry Senpai, you don't have the permissions for this command qwq")
        logging.error(error)


def setup(client):
    client.add_cog(error_handler(client))
