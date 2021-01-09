import discord, os, requests, json, challonge
from discord.ext import commands
from discord.utils import get

#https://api.challonge.com/v1
#https://github.com/ZEDGR/pychallonge

class Challonge(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Challonge cog loaded")

    @commands.group(invoke_without_command=True)
    async def challonge(self, ctx):
        await ctx.send("https://challonge.com/users/scuffedtourney/tournaments")

def setup(client):    
    client.add_cog(Challonge(client))