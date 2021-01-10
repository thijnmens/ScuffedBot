import discord, os, requests, json, challonge
from discord.ext import commands
from discord.utils import get

#https://api.challonge.com/v1
#https://github.com/ZEDGR/pychallonge

challonge.set_credentials("ScuffedTourney",os.getenv("CHALLONGEKEY"))

class Challonge(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Challonge cog loaded")

    @commands.group(invoke_without_command=True)
    async def challonge(self, ctx):
        await ctx.send("https://challonge.com/users/scuffedtourney/tournaments")

    @challonge.command()
    async def test(self, ctx):
        await ctx.send("okie dokie!")
        embed = discord.Embed(
            title = "ligma balls lol"
        )
        embed.set_image(url="https://challonge.com/l76djrwh.svg")
        await ctx.send(embed=embed)

def setup(client):    
    client.add_cog(Challonge(client))