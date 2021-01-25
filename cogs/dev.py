import discord
import os
import logging
from discord.ext import commands

devs = [
    490534335884165121,
    232574143818760192
]


def is_dev(user):
    if user in devs:
        return "valid"
    return "invalid"


class dev(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=["d"])
    async def dev (self, ctx):
        #I'll add something here when I have more time
        return logging.info(f"dev ran by {ctx.author.name}")

    @dev.command()
    async def load_cog (self, ctx, argument):
        logging.info(f"dev load_cog ran by {ctx.author.name}")
        if is_dev(ctx.author.id) == "invalid":
            logging.info("is_dev check returned invalid")
            return
        argument = "cog." + argument
        try:
            self.client.load_extension(argument)
            await ctx.send(f"loaded cog {argument}")
            logging.info(f"loaded cog {argument}")
        except Exception as e:
            await ctx.send(f"Failed to load cog {argument}: {e}")
            logging.error(f"Failed to load cog {argument}: {e}")

    @dev.command()
    async def unload_cog (self, ctx, argument):
        logging.info(f"dev unload_cog ran by {ctx.author.name}")
        if is_dev(ctx.author.id) == "invalid":
            logging.info("is_dev check returned invalid")
        argument = "cog." + argument
        try:
            self.client.unload_extension(argument)
            await ctx.send(f"unloaded cog {argument}")
            logging.info(f"unloaded cog {argument}")
        except Exception as e:
            await ctx.send(f"Failed to unload cog {argument}: {e}")
            logging.error(f"Failed to unload cog {argument}: {e}")

    @dev.command()
    async def shutdown (self, ctx):
        logging.info(f"dev shutdown ran by {ctx.author.name}")
        if is_dev(ctx.author.id) == "invalid":
            logging.info("is_dev check returned invalid")
        await ctx.send("Shutting down")
        logging.info("Shutting down")
        await self.client.close()


def setup(client):
    client.add_cog(dev(client))
