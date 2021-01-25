import discord
import os
import requests
import json
import challonge
import logging
from discord.ext import commands
from discord.utils import get

# https://api.challonge.com/v1
# https://github.com/ZEDGR/pychallonge

challonge.set_credentials("ScuffedTourney", os.getenv("CHALLONGEKEY"))


class challongeClient(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True,case_insensitive=True, aliases=["challenge", "ch"])
    @commands.cooldown(1, 60, commands.BucketType.channel)
    async def challonge(self, ctx):
        logging.info("recieved challonge")
        try:
            async with ctx.channel.typing():
                messages = ""
                tournaments = challonge.tournaments.index()
                count = 0
                par_count = 0
                for x in (tournaments):
                    tournament = tournaments[count]
                    if tournament["state"] == "pending" or tournament["state"] == "underway":
                        message = ("{} - ID: {}\nStatus: Tourney currently {}\n".format(
                            tournament["name"], tournament["id"], tournament["state"]))
                    else:
                        participants = challonge.participants.index(
                            tournament["id"])
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
                        message = (
                            "**[{}]({}) - ID: {}**\n1st: {}, 2nd: {}, 3rd: {}\n".format(
                                tournament["name"],
                                tournament["full_challonge_url"],
                                tournament["id"],
                                first,
                                second,
                                third))
                    messages = "\n" + message + messages
                    count = count + 1
                embed = discord.Embed(
                    title="Scuffed Tournaments",
                    url="https://challonge.com/users/scuffedtourney/tournaments",
                    description=messages,
                    colour=0xff7324,
                    timestamp=ctx.message.created_at)
            await ctx.send(embed=embed)
            logging.info("responded with embed")
        except Exception as e:
            logging.error(f"Uh Oh it did a fucky\n{e}")
            await ctx.send("I'm sorry, S-Senpai. I messed up your command qwq. Here's the challonge link instead >w< \n<https://challonge.com/users/scuffedtourney/tournaments>")
        logging.info("--------")

    @challonge.command()
    async def id(self, ctx, argument1=None):
        logging.info("recieved challonge id")
        if argument1 is None:
            await ctx.send("B-Baka!! You need to give a tournament ID!\n``Use >challonge to check the tournament IDs``")
            logging.info("No argument given")
            return
        try:
            tournament = challonge.tournaments.show(argument1)
        except Exception as e:
            logging.error(f"challonge id did a fucky when getting tournament\n{e}")
            await ctx.send("I'm sorry, S-Senpai. I messed up your command qwq. Here's the challonge link instead >w< \n<https://challonge.com/users/scuffedtourney/tournaments>")
        async with ctx.channel.typing():

            embed = discord.Embed(
                title=tournament["name"],
                url=tournament["full_challonge_url"],
                colour=0xff7324,
                timestamp=ctx.message.created_at
            )
        await ctx.send(embed=embed)
        logging.info("--------")


def setup(client):
    client.add_cog(challongeClient(client))
