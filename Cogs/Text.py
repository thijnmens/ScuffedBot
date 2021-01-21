import discord
import os
import json
import requests
from discord.ext import commands, tasks
from discord.utils import get


class Text(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Text cog loaded")

    # Commands List
    @commands.Cog.listener('on_message')
    async def on_message(self, message):
        if message.author == self.client.user:
            return

    # ping
    @commands.command()
    async def ping(self, ctx):
        print('Recieved: >ping')
        await ctx.send(f'uwu *notices your ping* <w< ``{round(self.client.latency * 1000)}ms``')
        print(f'Response: {round(self.client.latency * 1000)}')
        print('----------')

    @commands.command(aliases=["no"])  # Keep this out of the help embed ;)
    @commands.cooldown(1, 600, commands.BucketType.guild)
    async def nope(self, ctx):
        print("Recieved >nope")
        await ctx.send("Join the NOPE clan <:GunChamp:796047943966523432>\nhttps://discord.gg/xH7AGnGXkf")
        print("Response: Certainly not a link to the NOPE discord")
        print('----------')

    # Quote
    @commands.command()
    async def links(self, ctx):
        print('Recieved: >links')
        embed = discord.Embed(
            title="Important Scuffed Links",
            description="[Discord](https://discord.gg/4bF8JAGeB3) | [Challonge](https://challonge.com/users/scuffedtourney/tournaments) | [Scuffed Bot Repo](https://github.com/thijnmens/ScuffedBot)",
            color=0xff0000)
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/792019305755181057/797267487905021952/scuffed_as_hell.png")
        await ctx.send(embed=embed)
        print(f'Response: embed')
        print('----------')


def setup(client):
    client.add_cog(Text(client))
