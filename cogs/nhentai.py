# I made a bot for a bunch of horny retards
# https://pypi.org/project/NHentai-API/

import discord
import logging
import json
from discord.ext import commands
from NHentai import NHentai

nhentai = NHentai()


def sauce_embed(sauce):
    desc = "Tags: "
    for x in getattr(sauce, "tags"):
        desc = desc + x + ", "
    if "english" in getattr(sauce, "languages"):
        lang = "🇬🇧"
    elif "japanese" in getattr(sauce, "languages"):
        lang = "🇯🇵"
    elif "chinese" in getattr(sauce, "languages"):
        lang = "🇨🇳"
    else: 
        lang = "❔"
    embed = discord.Embed(
        title=f"{lang} "+getattr(sauce,"title"),
        url="https://nhentai.net/g/"+getattr(sauce,"id")+"/",
        description=desc,
        colour=0xec2753,
    )
    embed.set_footer(text=str(getattr(sauce,"total_pages"))+" total pages")
    embed.set_image(url=(getattr(sauce,"images"))[0])
    return embed


class nhen(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=["nh"])
    @commands.is_nsfw()
    async def nhentai(self, ctx, *, argument=None):
        logging.info("nhentai ran")
        #if not ctx.guild:
        #    await self.client.get_channel(754632208257515541).send(f"{ctx.author.name} is being lewd in my DMs! <a:GabiEmbarrased:807384551646560286>")
        if ctx.guild: #and ctx.channel.is_nsfw() is False:
            logging.info("Ran outside of nsfw channel\n----------")
            return await ctx.send("P-Pervert! <a:LoliTriggered:754632379397570620>")
        elif argument is None:
            sauce = nhentai.get_random()
            logging.info(sauce)
            await ctx.send(embed=sauce_embed(sauce))
            logging.info("Posted embed\n----------")
        elif argument.isdigit():
            sauce = nhentai._get_doujin(id=argument)
            logging.info(sauce)
            if sauce is None:
                return await ctx.send("S-Sorry, I can't find that id qwq")
            await ctx.send(embed=sauce_embed(sauce))
            logging.info("Posted embed\n----------")

def setup(client):
    client.add_cog(nhen(client))