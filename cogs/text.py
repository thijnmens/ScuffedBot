import discord
import os
import json
import requests
import logging
from discord.ext import commands, tasks
from discord.utils import get

aso = (580425653325791272)


class text(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener('on_message')
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        if self.client.user.mentioned_in(message):
            logging.info("Got pinged and annoyed Aso\n----------")
            await message.channel.send("<a:WeirdChamping:754632380219916319>")
            await self.client.get_user(aso).send("<a:MomoLewd:754632378701316179>")

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
            description="[Discord](https://discord.gg/4bF8JAGeB3) | [Challonge](https://challonge.com/users/scuffedtourney/tournaments) | [BeatKhana!](https://beatkhana.com/) | [Scuffed Bot Repo](https://github.com/thijnmens/ScuffedBot) |",
            color=0xff0000)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/796012513917272085/804784985961005073/hmm_yes_transparency.png")
        await ctx.send(embed=embed)
        logging.info(f'Response: embed----------')


def setup(client):
    client.add_cog(text(client))
