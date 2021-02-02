#I can assure you, this cog is vital for the performance and useability of Scuffed Bot

import discord
import logging
import requests
import asyncio 
import io
import aiohttp
import json
from discord.ext import commands

async def image(link):
    logging.info(f"image function ran with {link}")
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as resp:
            json_data = json.loads(await resp.text())
            logging.info(json_data["url"])
            async with session.get(json_data["url"]) as resp:
                return io.BytesIO(await resp.read())


class neko(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=["n"])
    async def neko(self, ctx):
        logging.info("neko ran")
        await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/neko"), "neko.png"))
        logging.info("attachment sent\n----------")
        
    @neko.command()
    async def gif(self, ctx):
        logging.info("neko gif ran")
        await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/ngif"), "neko.gif"))
        logging.info("attachment sent\n----------")

    @neko.group(invoke_without_command=True, case_insensitive=True)
    async def lewd(self, ctx):
        logging.info("neko lewd ran")
        if ctx.channel.is_nsfw() is False:
            logging.info("Ran outside of nsfw channel")
            return await ctx.send("P-Pervert! <a:LoliTriggered:754632379397570620>")
        await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/lewd"), "neko.png"))
        logging.info("attachment sent\n----------")

    @lewd.command()
    async def lewdgif(self, ctx):
        logging.info("neko lewd gif ran")
        if ctx.channel.is_nsfw() is False:
            logging.info("Ran outside of nsfw channel")
            return await ctx.send("P-Pervert! <a:LoliTriggered:754632379397570620>")
        await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/nsfw_neko_gif"), "neko.gif"))
        logging.info("attachment sent\n----------")


def setup(client):
    client.add_cog(neko(client))