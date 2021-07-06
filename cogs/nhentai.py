# https://pypi.org/project/NHentai-API/

from logging import info as logging_info

from discord import Embed

from discord.ext import commands
from NHentai.nhentai import NHentai


nhentai = NHentai()


async def sauce_embed(sauce):
    tags = str()
    for x in getattr(sauce, "tags"):
        tags = tags + x + ", "
    if tags == str():
        tags = "None"
    artist = str()
    for x in getattr(sauce, "artists"):
        artist = artist + x + ", "
    if artist == str():
        artist = "None"
    parodies = str()
    for x in getattr(sauce, "parodies"):
        parodies = parodies + x + ", "
    if artist == str():
        artist = "None"
    sec_title = "**Alternative Title:** "
    for x in getattr(sauce, "secondary_title"):
        sec_title = sec_title + x
    characters = str()
    for x in getattr(sauce, "characters"):
        characters = characters + x + ", "
    if artist == str():
        artist = "None"
    if "english" in getattr(sauce, "languages"):
        lang = "🇬🇧"
    elif "japanese" in getattr(sauce, "languages"):
        lang = "🇯🇵"
    elif "chinese" in getattr(sauce, "languages"):
        lang = "🇨🇳"
    else: 
        lang = "❔"
    embed = Embed(
        title=f"{lang} "+getattr(sauce,"title"),
        url="https://nhentai.net/g/"+getattr(sauce,"id")+"/",
        description=sec_title,
        colour=0xec2753,
    )
    embed.add_field(
        name="Tags",
        value=tags,
        inline=False
    )
    embed.add_field(
        name="Artists",
        value=artist,
        inline=True
    )
    if parodies:
        embed.add_field(
            name="Parodies",
            value=parodies,
            inline=True
        )
    if characters:
        embed.add_field(
            name="Characters",
            value=characters,
            inline=False
        )
    embed.set_footer(text=str(getattr(sauce,"total_pages"))+" total pages")
    embed.set_image(url=(getattr(sauce,"images"))[0])
    return embed


class NHentaiCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_nsfw()
    @commands.group(invoke_without_command=True, aliases=["nh"])
    async def nhentai(self, ctx, *, argument=None):
        if argument is None:
            sauce = nhentai.get_random()
            logging_info(sauce)
            await ctx.send(embed=await sauce_embed(sauce))
        elif argument.isdigit():
            sauce = nhentai.get_doujin(id=argument)
            logging_info(sauce)
            if sauce is None:
                return await ctx.send("S-Sorry, I can't find that id qwq")
            await ctx.send(embed=await sauce_embed(sauce))

    @nhentai.command()
    @commands.is_nsfw()
    async def search(self, ctx, argument=None, val=1):
        val = val - 1
        if argument is None:
            logging_info("nothing provided lmao")
            return await ctx.send("S-Sorry, but I can't search for nothing qwq")
        if argument.isalpha():
            SearchPage = nhentai.search(query=argument, sort='popular', page=1)
            Doujin = getattr(SearchPage, "doujins")
            logging_info(Doujin)
            if not Doujin:
                logging_info("nothing found lmao what a dumbass")
                return await ctx.send("S-Sorry, I can't find anything qwq")
            await ctx.send(embed=await sauce_embed(nhentai.get_doujin(id=getattr(Doujin[int(val)], "id"))))

def setup(bot):
    bot.add_cog(NHentaiCog(bot))
