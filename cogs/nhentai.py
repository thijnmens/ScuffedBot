# I made a bot for a bunch of horny retards

import discord
import logging
import json
from discord.ext import commands
from NHentai import NHentai

nhentai = NHentai()

#killme = (nhentai.get_random())
#print (getattr(killme, "title"))



class nhen(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=["nh"])
    async def nhentai(self, ctx, argument=None):
        logging.info("nhentai ran")
        if ctx.channel.is_nsfw() is False:
            logging.info("Ran outside of nsfw channel\n----------")
            return await ctx.send("P-Pervert! <a:LoliTriggered:754632379397570620>")
        if argument is None:
            sauce = nhentai.get_random()
            logging.info(sauce)
            embed = discord.Embed(
                title=getattr(sauce,"title"),
                url="https://nhentai.net/g/"+getattr(sauce,"id")+"/",
                description=getattr(sauce,"tags"),
                colour=0xec2753,
                timestamp=getattr(sauce,"total_pages")+" total pages"
            )
            embed.set_image(url=(getattr(sauce,"images"))[0])
            await ctx.send(embed=embed)
            logging.info("Posted embed\n----------")


def setup(client):
    client.add_cog(nhen(client))