from logging import info as logging_info, error as logging_error
from os import getenv

from discord import Embed
from challonge import set_credentials

from challonge.tournaments import index as tournaments_index, show
from challonge.participants import index as participants_index
from discord.ext import commands

# https://api.challonge.com/v1
# https://github.com/ZEDGR/pychallonge

set_credentials("ScuffedTourney", getenv("CHALLONGEKEY"))


class challongebot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, aliases=["challenge", "ch"])
    @commands.cooldown(1, 60, commands.BucketType.channel)
    async def challonge(self, ctx):
        try:
            async with ctx.channel.typing():
                messages = ""
                tournaments = tournaments_index()
                count = (len(tournaments) - 4)
                par_count = 0
                #for x in (tournaments):
                for x in range(0, 4):
                    tournament = tournaments[count]
                    if tournament["state"] == "pending" or tournament["state"] == "underway":
                        message = ("{} - ID: {}\nStatus: Tourney currently {}\n".format(
                            tournament["name"], tournament["id"], tournament["state"]))
                    else:
                        participants = participants_index(
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
                                third)
                            )
                    messages = "\n" + message + messages
                    count = count + 1
                embed = Embed(
                    title="Scuffed Tournaments",
                    url="https://challonge.com/users/scuffedtourney/tournaments",
                    description=messages,
                    colour=0xff7324,
                    timestamp=ctx.message.created_at)
            await ctx.send(embed=embed)
            logging_info("responded with embed")
        except Exception as e:
            logging_error(f"Uh Oh it did a fucky\n{e}")
            await ctx.send("I'm sorry, S-Senpai. I messed up your command qwq. Here's the challonge link instead >w< \n<https://challonge.com/users/scuffedtourney/tournaments>")

    @challonge.command()
    async def id(self, ctx, argument1=None):
        if argument1 is None:
            await ctx.send("B-Baka!! You need to give a tournament ID!\n``Use >challonge to check the tournament IDs``")
            logging_info("No argument given")
            return
        try:
            tournament = show(argument1)
        except Exception as e:
            logging_error(f"challonge id did a fucky when getting tournament\n{e}")
            await ctx.send("I'm sorry, S-Senpai. I messed up your command qwq. Here's the challonge link instead >w< \n<https://challonge.com/users/scuffedtourney/tournaments>")
        async with ctx.channel.typing():

            embed = Embed(
                title=tournament["name"],
                url=tournament["full_challonge_url"],
                colour=0xff7324,
                timestamp=ctx.message.created_at
            )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(challongebot(bot))
