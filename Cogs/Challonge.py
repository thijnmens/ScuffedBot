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
        print ("recieved challonge")
        async with ctx.channel.typing():
            messages = ""
            tournaments = challonge.tournaments.index()
            count = 0
            for x in tournaments:
                tournament = tournaments[count]
                tourney_name = (tournament["name"])
                matches = challonge.matches.index(tournament["id"])
                if (len(matches)) == 0:
                    winner = ("not determined")
                else:
                    match = matches[(len(matches)) - 1]
                    winner = challonge.participants.show(tournament["id"], match["winner_id"])
                    winner = ("1st: {}".format(winner["name"]))
                message = (f"{tourney_name} - Winner: {winner}")
                messages = messages+message
                count = count + 1
            embed=discord.Embed(
                title = "Scuffed Tournaments",
                url = "https://challonge.com/users/scuffedtourney/tournaments",
                description = messages,
                colour = 0xff7324,
                timestamp = ctx.message.created_at
            )
            await ctx.send(embed=embed)
        print ("responded with embed")
        print ("--------")

def setup(client):    
    client.add_cog(Challonge(client))