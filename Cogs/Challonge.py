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

    @commands.group(invoke_without_command=True, aliases=["challenge", "ch"])
    async def challonge(self, ctx):
        print ("recieved challonge")
        try:
            async with ctx.channel.typing():
                messages = ""
                tournaments = challonge.tournaments.index()
                count = 0
                par_count = 0
                for x in (tournaments):
                    tournament = tournaments[count]
                    if tournament["state"] == "pending" or tournament["state"] == "underway":
                        message = ("```{} - ID: {}\nStatus: {}```".format(tournament["name"],tournament["id"],tournament["state"]))
                    else:
                        embed=discord.Embed(
                            title = "Scuffed Tournaments",
                            url = "https://challonge.com/users/scuffedtourney/tournaments",
                            #description = messages,
                            colour = 0xff7324,
                            timestamp = ctx.message.created_at
                        )
                        participants = challonge.participants.index(tournament["id"])
                        for x in participants:
                            participant = participants[par_count]
                            if participant["final_rank"] == 1:
                                first = participant["name"]
                            elif participant["final_rank"] == 2:
                                second = participant["name"]
                            elif participant["final_rank"] == 3:
                                third = participant["name"]
                            par_count = par_count + 1
                        par_count = 0 
                        message = ("```{} - ID: {}\n1st: {}, 2nd: {}, 3rd: {}```".format(tournament["name"],tournament["id"],first, second, third))
                        name = "[{}]({})".format(tournament["name"], tournament["full_challonge_url"])
                        value = "1st: {}, 2nd: {}, 3rd: {}".format(first, second, third)
                        embed.add_field(name=name, value=value, inline=False)
                    messages = message+messages
                    count = count + 1

                await ctx.send(embed=embed)
                print ("responded with embed")
        except Exception as e:
            print (f"Uh Oh it did a fucky\n{e}")
            await ctx.send("I'm sorry, S-Senpai. I messed up your command qwq. Here's the challonge link instead >w< \n<https://challonge.com/users/scuffedtourney/tournaments>")
        print ("--------")

    @challonge.command()
    async def id (self, ctx, argument1=None):
        print ("recieved challonge id")
        if argument1 is None:
            await ctx.send("B-Baka!! You need to give a tournament ID!\n``Use >challonge to check the tournament IDs``")
            print ("No argument given")
            return
        try:
            tournament = challonge.tournaments.show(argument1)
        except Exception as e:
            print (f"challonge id did a fucky when getting tournament\n{e}")
            await ctx.send("I'm sorry, S-Senpai. I messed up your command qwq. Here's the challonge link instead >w< \n<https://challonge.com/users/scuffedtourney/tournaments>")
        async with ctx.channel.typing():
            
            embed=discord.Embed(
                title = tournament["name"],
                url = tournament["full_challonge_url"],
                colour = 0xff7324,
                timestamp = ctx.message.created_at
            )
            await ctx.send(embed=embed)
        print ("--------")

def setup(client):    
    client.add_cog(Challonge(client))