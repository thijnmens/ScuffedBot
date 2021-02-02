#I can assure you, this cog is vital for the performance and useability of Scuffed Bot

import discord
import logging
import requests
import asyncio 
import io
import aiohttp
import json
from discord.ext import commands


class neko(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def neko(self, ctx):
        logging.info("neko ran")
        async with aiohttp.ClientSession() as session:
            async with session.get("https://nekos.life/api/v2/img/neko") as resp:
                json_data = json.loads(await resp.text())
                logging.info(json_data["url"])
                async with session.get(json_data["url"]) as resp:
                    await ctx.send(file=discord.File((io.BytesIO(await resp.read())), "neko.png"))
        

def setup(client):
    client.add_cog(neko(client))