import discord
import os
import requests
import json
import firebase_admin
import logging
from random import randint
from discord.ext import commands, menus
from discord.utils import get
from firebase_admin import credentials, firestore, db

dab = firestore.client()
header = {
    "User-Agent": "Scuffed Bot (https://github.com/thijnmens/ScuffedBot)"
}

SS_id = None
page = int(0)
# https://new.scoresaber.com/api/player/76561198091128855/full
# https://new.scoresaber.com/api/static/covers/69E494F4A295197BF03720029086FABE6856FBCE.png
# URL = (f"https://new.scoresaber.com/api/player/{SS_id}/full") - Get UserData
# URL = (f"https://new.scoresaber.com/api/player/{SS_id}/scores/top/{page}") - #Get Top Songs
# URL = (f"https://new.scoresaber.com/api/player/{SS_id}/scores/recent/{page}") - #Get Recent Songs
# URL = (f"https://new.scoresaber.com/api/players/{page}") - #Get Global Rankings
# URL = (f"https://new.scoresaber.com/api/players/pages") - #Get Global
# Ranking Pages


# Makes the embed message for topSong and recentSong
def songEmbed(ctx, argument, SS_id, scoresaber):
    if argument == "recentSong":
        URL = (f"https://new.scoresaber.com/api/player/{SS_id}/scores/recent")
    elif argument == "topSong":
        URL = (f"https://new.scoresaber.com/api/player/{SS_id}/scores/top")
    URL1 = (f"https://new.scoresaber.com/api/player/{SS_id}/full")
    logging.info(URL+"\n"+URL1)
    response = requests.get(URL, headers=header)
    json_data = json.loads(response.text)
    if "error" in json_data:
        message = discord.Embed(
            title="Uh Oh, the codie wodie did an oopsie woopsie! uwu",
            description="Check if your ScoreSaber link is valid <:AYAYASmile:789578607688417310>",
            colour=0xff0000)
        return message
    songsList = json_data["scores"]
    response = requests.get(URL1, headers=header)
    json_data = json.loads(response.text)
    playerInfo = json_data["playerInfo"]
    playerName = playerInfo["playerName"]
    Song = songsList[0]
    songName = Song["songName"]
    songSubName = Song["songSubName"]
    songAuthorName = Song["songAuthorName"]
    levelAuthorName = Song["levelAuthorName"]
    timeSet = Song["timeSet"]
    songHash = Song["songHash"]
    URL2 = (f"https://beatsaver.com/api/maps/by-hash/{songHash}")  # Beat Saver
    # URL2 = (f"https://maps.beatsaberplus.com/api/maps/by-hash/{songHash}")
    # #HardCPP's Mirror
    response = requests.get(URL2, headers=header)
    json_data = json.loads(response.text)
    songKey = json_data["key"]
    songBSLink = (f"https://beatsaver.com/beatmap/{songKey}")
    if Song["maxScore"] == 0:
        acc = randint(0, 100)
        songAcc = f"ScoreSaber API being fucky wucky,\nso you get {acc}"
    else:
        songAcc = round((int(Song["score"]) / int(Song["maxScore"])) * 100, 2)
    rank = Song["rank"]
    if Song["difficulty"] == 9:
        difficulty = "<:ExpertPlus1:794900253156442134><:ExpertPlus2:794900231883063297><:ExpertPlus3:794900212060520448>"
    elif Song["difficulty"] == 7:
        difficulty = "<:Expert1:794900190623957032><:Expert2:794900172647301122>"
    elif Song["difficulty"] == 5:
        difficulty = "<:hard1:794900135099629568><:Hard2:794900117726822400>"
    elif Song["difficulty"] == 3:
        difficulty = "<:Normal1:794900081135845379><:Normal2:794900048706142218><:Normal3:794899993701908522>"
    elif Song["difficulty"] == 1:
        difficulty = "<:Easy1:794899950713438239><:Easy2:794899950655111186>"
    else:
        difficulty = "Please ping Sirspam thanks uwu"
    if songSubName == '':
        title = f"{songName}"
    else:
        title = f"{songName} - {songSubName}"
    message = discord.Embed(
        title=title,
        url=songBSLink,
        description=f"**{songAuthorName} - {levelAuthorName}** {difficulty}",
        colour=0xffdc1b,
        timestamp=ctx.message.created_at
    )
    message.set_author(
        name=playerName,
        url=scoresaber,
        icon_url="https://new.scoresaber.com" +
        playerInfo["avatar"])
    message.add_field(
        name="Rank <a:PeepoBoing1:792487937056571392><a:PeepoBoing2:792487937257766912><a:PeepoBoing3:792487937044512768>",
        value=f"#{rank}",
        inline=False)
    message.add_field(
        name="Acc <:WideAcc1:792487936691535893><:WideAcc2:792487936640811028><:WideAcc3:792487936314572811><:WideAcc4:792487936636616826>",
        value=f"{songAcc}%",
        inline=False)
    message.add_field(
        name="Score <:AquaCollapsed1:792487936658243614><:AquaCollapsed2:792487936272367648><:AquaCollapsed3:792487936829816863>",
        value=Song["score"],
        inline=False)
    if Song["pp"] == 0:
        message.add_field(
            name="PP <a:BurgerChamp1:792487936703725600><a:BurgerChamp2:792487936280756246><a:BurgerChamp3:792487936679215134><a:BurgerChamp4:792487936771489832>",
            value="Unranked",
            inline=False)
    else:
        message.add_field(
            name="PP <a:BurgerChamp1:792487936703725600><a:BurgerChamp2:792487936280756246><a:BurgerChamp3:792487936679215134><a:BurgerChamp4:792487936771489832>",
            value=round(
                Song["pp"],
                2),
            inline=False)
        message.add_field(
            name="Weighted PP ⚖️<a:BurgerChamp1:792487936703725600><a:BurgerChamp2:792487936280756246><a:BurgerChamp3:792487936679215134><a:BurgerChamp4:792487936771489832>",
            value=round((Song["weight"] * Song["pp"]),2),
            inline=False)
    message.add_field(name="Time Set 🕕🕘", value=timeSet[:10], inline=False)
    message.set_image(url="https://new.scoresaber.com/api/static/covers/" + Song["songHash"] + ".png")
    return message


def songsEmbed(ctx, argument, SS_id, scoresaber):
    if argument == "recentSongs":
        URL = (f"https://new.scoresaber.com/api/player/{SS_id}/scores/recent")
        requestType = ("Recent Songs")
    elif argument == "topSongs":
        URL = (f"https://new.scoresaber.com/api/player/{SS_id}/scores/top")
        requestType = ("Top Songs")
    URL1 = (f"https://new.scoresaber.com/api/player/{SS_id}/full")
    logging.info(URL+"\n"+URL1)
    response = requests.get(URL, headers=header)
    json_data = json.loads(response.text)
    if "error" in json_data:
        message = discord.Embed(
            title="Uh Oh, the codie wodie did an oopsie woopsie! uwu",
            description="Check if your ScoreSaber link is valid <:AYAYASmile:789578607688417310>",
            colour=0xff0000)
        return message
    songsList = json_data["scores"]
    response = requests.get(URL1, headers=header)
    json_data = json.loads(response.text)
    playerInfo = json_data["playerInfo"]
    playerName = playerInfo["playerName"]
    songsMessage = ""
    count = 0
    while count != len(songsList):
        Song = songsList[count]
        songName = Song["songName"]
        songSubName = Song["songSubName"]
        if songSubName == '':
            songTitle = f"{songName}"
        else:
            songTitle = f"{songName} - {songSubName}"
        songAuthorName = Song["songAuthorName"]
        levelAuthorName = Song["levelAuthorName"]
        rank = Song["rank"]
        songScore = Song["score"]
        timeSet = Song["timeSet"]
        if Song["maxScore"] == 0:
            acc = randint(0, 100)
            songAcc = f"ScoreSaber API being fucky wucky, so you get {acc}"
        else:
            songAcc = round((int(songScore) / int(Song["maxScore"])) * 100, 2)
        if Song["pp"] == 0:
            songPP = "Unranked"
            songWeightedPP = "Unranked"
        else:
            songPP = Song["pp"]
            songPP == round(songPP, 2)
            songWeightedPP = round((Song["weight"] * Song["pp"]), 2)
        if Song["difficulty"] == 9:
            difficulty = "Expert+"
        elif Song["difficulty"] == 7:
            difficulty = "Expert"
        elif Song["difficulty"] == 5:
            difficulty = "Hard"
        elif Song["difficulty"] == 3:
            difficulty = "Normal"
        elif Song["difficulty"] == 1:
            difficulty = "Easy"
        else:
            difficulty = "Please ping Sirspam thanks uwu"
        songMessage = (
            f"```Song: {songTitle}, {songAuthorName} - {levelAuthorName} ({difficulty})\nRank: #{rank}\nAcc: {songAcc}%\nScore: {songScore}\nPP: {songPP}\nWeighted PP: {songWeightedPP}\nTime Set: {timeSet[:10]}```")
        songsMessage = songsMessage + songMessage
        count = count + 1
    message = discord.Embed(
        title=f"{playerName}'s {requestType}",
        url=scoresaber,
        description=songsMessage,
        colour=0xffdc1b,
        timestamp=ctx.message.created_at
    )
    return message


class scoresaber(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=["ss"])
    async def scoresaber(self, ctx, argument1=None):
        logging.info(f"Recieved >scoresaber {ctx.author.name}")
        if argument1 is not None:
            if argument1.isdigit():
                ctx.author = self.client.get_user(int(argument1))
                if ctx.author is None:
                    return await ctx.send("Sorry Senpai, I can't find anyone with that ID qwq")
            else:
                ID = argument1[3:]
                ID = ID[:-1]
                ctx.author = self.client.get_user(int(ID))
                if ctx.author is None:
                    return await ctx.send("Sorry Senpai, I can't find anyone with that ID qwq")
            logging.info(f"Argument given, now {ctx.author.name}")
        async with ctx.channel.typing():
            ref = dab.collection("users").document(str(ctx.author.id)).get()
            scoresaber = ref.get('scoresaber')
            SS_id = scoresaber[25:]
            URL = (f"https://new.scoresaber.com/api/player/{SS_id}/full")
            logging.info(URL)
            response = requests.get(URL, headers=header)
            json_data = json.loads(response.text)
            if "error" in json_data:
                return await ctx.send("Uh Oh, the codie wodie did an oopsie! uwu\nCheck if your ScoreSaber link is valid <:AYAYASmile:789578607688417310>")
            playerInfo = json_data["playerInfo"]
            scoreStats = json_data["scoreStats"]
            playerCountry = playerInfo["country"]
            playerName = playerInfo["playerName"]
            playerCountryFlag = (f":flag_{playerCountry.lower()}:")
            rankedAcc = round(scoreStats["averageRankedAccuracy"], 2)
            embed = discord.Embed(
                title=f"{playerName}'s ScoreSaber Stats <:WidePeepoHappy1:757948845362511992><:WidePeepoHappy2:757948845404585984><:WidePeepoHappy3:757948845400522812><:WidePeepoHappy4:757948845463306310>",
                url=scoresaber,
                colour=0xffdc1b,
                timestamp=ctx.message.created_at
            )
            embed.add_field(
                name="Global Rank 🌐",
                value=playerInfo["rank"],
                inline=True)
            embed.add_field(
                name=f"Country Rank {playerCountryFlag}",
                value=playerInfo["countryRank"],
                inline=True)
            embed.add_field(
                name="PP <a:PogLick:792002791828357131>",
                value=playerInfo["pp"],
                inline=True)
            embed.add_field(
                name="Ranked Acc <:PeepoAcc:792385194351001610>",
                value=f"{rankedAcc}%",
                inline=True)
            embed.add_field(
                name="Total Play Count <a:ppJedi:754632378206388315>",
                value=scoreStats["totalPlayCount"],
                inline=True)
            embed.add_field(
                name="Ranked Play Count 🧑‍🌾",
                value=scoreStats["rankedPlayCount"],
                inline=True)
            embed.set_thumbnail(
                url="https://new.scoresaber.com" + playerInfo["avatar"])
        await ctx.send(embed=embed)
        logging.info("Response: ScoreSaber UserData embed\n----------")

    @scoresaber.command(aliases=["rs"])
    async def recentsong(self, ctx, argument1=None):
        logging.info(f"Recieved >scoresaber recentsong {ctx.author.name}")
        if argument1 is not None:
            if argument1.isdigit():
                ctx.author = self.client.get_user(int(argument1))
                if ctx.author is None:
                    return await ctx.send("Sorry Senpai, I can't find anyone with that ID qwq")
            else:
                ID = argument1[3:]
                ID = ID[:-1]
                ctx.author = self.client.get_user(int(ID))
                if ctx.author is None:
                    return await ctx.send("Sorry Senpai, I can't find anyone with that ID qwq")
            logging.info(f"Argument given, now {ctx.author.name}")
        async with ctx.channel.typing():
            ref = dab.collection("users").document(str(ctx.author.id)).get()
            scoresaber = ref.get('scoresaber')
            SS_id = scoresaber[25:]
            argument = "recentSong"
        await ctx.send(embed=songEmbed(ctx, argument, SS_id, scoresaber))
        logging.info("Response: ScoreSaber RecentSong embed\n----------")

    @scoresaber.command(aliases=["ts"])
    async def topsong(self, ctx, argument1=None):
        logging.info(f"Recieved >scoresaber topsong {ctx.author.name}")
        if argument1 is not None:
            if argument1.isdigit():
                ctx.author = self.client.get_user(int(argument1))
                if ctx.author is None:
                    return await ctx.send("Sorry Senpai, I can't find anyone with that ID qwq")
            else:
                ID = argument1[3:]
                ID = ID[:-1]
                ctx.author = self.client.get_user(int(ID))
                if ctx.author is None:
                    return await ctx.send("Sorry Senpai, I can't find anyone with that ID qwq")
            logging.info(f"Argument given, now {ctx.author.name}")
        async with ctx.channel.typing():
            ref = dab.collection("users").document(str(ctx.author.id)).get()
            scoresaber = ref.get('scoresaber')
            SS_id = scoresaber[25:]
            argument = "topSong"
        await ctx.send(embed=songEmbed(ctx, argument, SS_id, scoresaber))
        logging.info("Response: ScoreSaber TopSong embed\n----------")

    @scoresaber.command(aliases=["rss"])
    async def recentsongs(self, ctx, argument1=None):
        if argument1 is not None:
            if argument1.isdigit():
                ctx.author = self.client.get_user(int(argument1))
                if ctx.author is None:
                    return await ctx.send("Sorry Senpai, I can't find anyone with that ID qwq")
            else:
                ID = argument1[3:]
                ID = ID[:-1]
                ctx.author = self.client.get_user(int(ID))
                if ctx.author is None:
                    return await ctx.send("Sorry Senpai, I can't find anyone with that ID qwq")
            logging.info(f"Argument given, now {ctx.author.name}")
        async with ctx.channel.typing():
            ref = dab.collection("users").document(str(ctx.author.id)).get()
            scoresaber = ref.get('scoresaber')
            SS_id = scoresaber[25:]
            argument = "recentSongs"
        await ctx.send(embed=songsEmbed(ctx, argument, SS_id, scoresaber))
        logging.info("Response: ScoreSaber RecentSongs embed\n----------")

    @scoresaber.command(aliases=["tss"])
    async def topsongs(self, ctx, argument1=None):
        if argument1 is not None:
            if argument1.isdigit():
                ctx.author = self.client.get_user(int(argument1))
                if ctx.author is None:
                    return await ctx.send("Sorry Senpai, I can't find anyone with that ID qwq")
            else:
                ID = argument1[3:]
                ID = ID[:-1]
                ctx.author = self.client.get_user(int(ID))
                if ctx.author is None:
                    return await ctx.send("Sorry Senpai, I can't find anyone with that ID qwq")
            logging.info(f"Argument given, now {ctx.author.name}")
        async with ctx.channel.typing():
            ref = dab.collection("users").document(str(ctx.author.id)).get()
            scoresaber = ref.get('scoresaber')
            SS_id = scoresaber[25:]
            argument = "topSongs"
        await ctx.send(embed=songsEmbed(ctx, argument, SS_id, scoresaber))
        logging.info("Response: ScoreSaber TopSongs embed\n----------")

    @scoresaber.command()
    async def compare(self, ctx, argument1=None, argument2=None):
        if argument1 is None or argument2 is None:
            await ctx.send("You need to mention two people for me to compare!")
            return
        return


def setup(client):
    client.add_cog(scoresaber(client))
