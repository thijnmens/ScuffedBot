# I made a bot for a bunch of horny retards
# https://pypi.org/project/NHentai-API/

import discord
import logging
from discord.ext import commands
from NHentai import NHentai

nhentai = NHentai()


async def sauce_embed(sauce):
    print(sauce)
    Tags = "Tags: "
    for x in getattr(sauce, "tags"):
        Tags = Tags + x + ", "
    Artist = "Artist: "
    for y in getattr(sauce, "artists"):
        Artist = Artist + y + ", "
    Parodies = "Parodies: "
    for z in getattr(sauce, "parodies"):
        Parodies = Parodies + z + ", "
    sec_title = "Alternative Title: "
    for a in getattr(sauce, "secondary_title"):
        sec_title = sec_title + a 
    characters = "Characters: "
    for b in getattr(sauce, "characters"):
        characters = characters + b + ", "
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
        description=sec_title,
        colour=0x1f13ee,
    )
    embed.add_field(
        name="Tags",
        value=Tags,
        inline=False
    )
    embed.add_field(
        name="Artist",
        value=Artist,
        inline=False
    )
    embed.add_field(
        name="Parodies",
        value=Parodies,
        inline=False
    )
    embed.add_field(
        name="Characters",
        value=characters,
        inline=False
    )
    embed.set_footer(text=str(getattr(sauce,"total_pages"))+" total pages")
    embed.set_image(url=(getattr(sauce,"images"))[0])
    return embed


class nhen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_nsfw()
    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=["nh"])
    async def nhentai(self, ctx, *, argument=None):
        logging.info("nhentai ran")
        if not ctx.guild:
            await self.bot.get_channel(754632208257515541).send(f"{ctx.author.name} is being lewd in my DMs! <a:GabiEmbarrased:807384551646560286>")
        elif argument is None:
            sauce = nhentai.get_random()
            logging.info(sauce)
            await ctx.send(embed=await sauce_embed(sauce))
            logging.info("Posted embed\n----------")
        elif argument.isdigit():
            sauce = nhentai._get_doujin(id=argument)
            logging.info(sauce)
            if sauce is None:
                return await ctx.send("S-Sorry, I can't find that id qwq")
            await ctx.send(embed=await sauce_embed(sauce))
            logging.info("Posted embed\n----------")

def setup(bot):
    bot.add_cog(nhen(bot))
