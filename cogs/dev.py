import discord
import os
import logging
from discord.ext import commands


class dev(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=["d"])
    @commands.has_role(797422816584007720)
    async def dev (self, ctx):
        #I'll add something here when I have more time
        if ctx.invoked_subcommand is None:
            await ctx.send("haha look at this handling the error! yep, it's doing a great job!!\nHey user, be better and stop raising errors. k thanks uwu")
        return logging.info(f"dev ran by {ctx.author.name}")

    @dev.command()
    @commands.has_role(797422816584007720)
    async def load_cog (self, ctx, argument):
        logging.info(f"dev load_cog ran by {ctx.author.name}")
        argument = "cogs." + argument
        try:
            self.client.load_extension(argument)
            await ctx.send(f"loaded cog {argument}")
            logging.info(f"loaded cog {argument}")
        except Exception as e:
            await ctx.send(f"Failed to load cog {argument}: {e}")
            logging.error(f"Failed to load cog {argument}: {e}")

    @dev.command()
    @commands.has_role(797422816584007720)
    async def unload_cog (self, ctx, argument):
        logging.info(f"dev unload_cog ran by {ctx.author.name}")
        argument = "cogs." + argument
        try:
            self.client.unload_extension(argument)
            await ctx.send(f"unloaded cog {argument}")
            logging.info(f"unloaded cog {argument}")
        except Exception as e:
            await ctx.send(f"Failed to unload cog {argument}: {e}")
            logging.error(f"Failed to unload cog {argument}: {e}")

    @dev.command()
    @commands.has_role(797422816584007720)
    async def shutdown (self, ctx):
        logging.info(f"dev shutdown ran by {ctx.author.name}")
        await ctx.send("Shutting down")
        logging.info("Shutting down")
        await self.client.close()


def setup(client):
    client.add_cog(dev(client))
