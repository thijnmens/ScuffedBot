import discord
import os
import json
import requests
import logging
from discord.ext import commands, tasks
from discord.utils import get


class text(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Commands List
    @commands.Cog.listener('on_message')
    async def on_message(self, message):
        if message.author == self.client.user:
            return

    # ping
    @commands.command(case_insensitive=True)
    async def ping(self, ctx):
        logging.info('Recieved: >ping')
        await ctx.send(f'uwu *notices your ping* <w< ``{round(self.client.latency * 1000)}ms``')
        logging.info(f'Response: {round(self.client.latency * 1000)}ms\n----------')

    @commands.command(case_insensitive=True, aliases=["no"])  # Keep this out of the help embed ;)
    @commands.cooldown(1, 600, commands.BucketType.guild)
    async def nope(self, ctx):
        logging.info("Recieved >nope")
        await ctx.send("Join the NOPE clan <:GunChamp:796047943966523432>\nhttps://discord.gg/xH7AGnGXkf")
        logging.info("Response: Certainly not a link to the NOPE discord----------")

    # Quote
    @commands.command(case_insensitive=True)
    async def links(self, ctx):
        logging.info('Recieved: >links')
        embed = discord.Embed(
            title="Important Scuffed Links",
            description="[Discord](https://discord.gg/4bF8JAGeB3) | [Challonge](https://challonge.com/users/scuffedtourney/tournaments) | [Scuffed Bot Repo](https://github.com/thijnmens/ScuffedBot)",
            color=0xff0000)
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/792019305755181057/797267487905021952/scuffed_as_hell.png")
        await ctx.send(embed=embed)
        logging.info(f'Response: embed----------')


def setup(client):
    client.add_cog(text(client))
