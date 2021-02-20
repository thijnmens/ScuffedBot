# https://new.scoresaber.com/api/player/76561198091128855/full
# https://new.scoresaber.com/api/static/covers/69E494F4A295197BF03720029086FABE6856FBCE.png
# URL = (f"https://new.scoresaber.com/api/player/{SS_id}/full") - Get UserData
# URL = (f"https://new.scoresaber.com/api/player/{SS_id}/scores/top/{page}") - #Get Top Songs
# URL = (f"https://new.scoresaber.com/api/player/{SS_id}/scores/recent/{page}") - #Get Recent Songs
# URL = (f"https://new.scoresaber.com/api/players/{page}") - #Get Global Rankings
# URL = (f"https://new.scoresaber.com/api/players/pages") - #Get Global
# Ranking Pages


import discord
import requests
import json
import logging
from random import randint
from discord.ext import commands
from discord.utils import get
from firebase_admin import firestore


dab = firestore.client()
header = {
    "User-Agent": "Scuffed Bot (https://github.com/thijnmens/ScuffedBot)"
}
SS_id = None


# Returns the ID for the user given
async def userID(self, argument):
    if argument.isdigit():
        return self.client.get_user(int(argument))
    else:
        ID = argument[3:]
        ID = ID[:-1]
        return self.client.get_user(int(ID))

# Makes the embed message for topSong and recentSong
async def songEmbed(self, ctx, arg_page, arg_user, type):
    if arg_user is not None:
        ctx.author = await userID(self, arg_user)
        logging.info(f"Argument given, now {ctx.author.name}")
    if ctx.author is None:
        logging.info("ctx.author is None")
        return await ctx.send("Sorry Senpai, I can't find anyone with that ID qwq")
    ref = dab.collection("users").document(str(ctx.author.id)).get()
    scoresaber = ref.get('scoresaber')
    if scoresaber is None:
        await ctx.send("Sorry Senpai, that user isn't in my database!")
        return logging.info("scoresaber is None")
    SS_id = scoresaber[25:]
    page = (arg_page / 8)
    if page.is_integer() is False:
        page = int(page + 1)
    else:
        page = int(page)
    if type == "recentSong":
        URL = (f"https://new.scoresaber.com/api/player/{SS_id}/scores/recent/{page}")
    elif type == "topSong":
        URL = (f"https://new.scoresaber.com/api/player/{SS_id}/scores/top/{page}")
    URL1 = (f"https://new.scoresaber.com/api/player/{SS_id}/full")
    logging.info(URL+"\n"+URL1)
    try: 
        json_data = json.loads(requests.get(URL, headers=header).text)
    except:
        logging.info(f"scoresaber api returned nothing, probably getting hammered lol")
        return await ctx.send("Sorry Senpai, ScoreSaber-chan is busy right now!\nTry again later ^w^")
    print(f"json data: '{json_data}'")
    if "error" in json_data:
        logging.info(f"scoresaber api returned an error\n{json_data}")
        return await ctx.send("Uh Oh, the codie wodie did an oopsie woopsie! uwu\nCheck if your ScoreSaber link is valid <:AYAYASmile:789578607688417310>")
    songsList = json_data["scores"]
    json_data = json.loads(requests.get(URL1, headers=header).text)
    playerInfo = json_data["playerInfo"]
    if page > 1:
        while arg_page >= 8:
            arg_page = (arg_page - 8)
    Song = songsList[(arg_page - 1)]
    URL2 = (f"https://beatsaver.com/api/maps/by-hash/"+Song["songHash"])
    json_data = json.loads(requests.get(URL2, headers=header).text)
    songBSLink = (f"https://beatsaver.com/beatmap/"+json_data["key"])
    if Song["maxScore"] == 0:
        songAcc = f"ScoreSaber API being fucky wucky,\nso you get {randint(0, 100)}"
    else:
        songAcc = round((int(Song["score"]) / int(Song["maxScore"])) * 100, 2)
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
    if Song["songSubName"] == '':
        title = Song["songName"]
    else:
        title = Song["songName"]+" - "+Song["songSubName"]
    message = discord.Embed(
        title=title,
        url=songBSLink,
        description="**"+Song["songAuthorName"]+" - "+Song["levelAuthorName"]+f"** {difficulty}",
        colour=0xffdc1b,
        timestamp=ctx.message.created_at
    )
    message.set_author(
        name=playerInfo["playerName"],
        url=scoresaber,
        icon_url="https://new.scoresaber.com" +
        playerInfo["avatar"]
    )
    message.add_field(
        name="Rank <a:PeepoBoing1:792487937056571392><a:PeepoBoing2:792487937257766912><a:PeepoBoing3:792487937044512768>",
        value="#"+str(Song["rank"]),
        inline=False
    )
    message.add_field(
        name="Acc <:WideAcc1:792487936691535893><:WideAcc2:792487936640811028><:WideAcc3:792487936314572811><:WideAcc4:792487936636616826>",
        value=f"{songAcc}%",
        inline=False
    )
    message.add_field(
        name="Score <:AquaCollapsed1:792487936658243614><:AquaCollapsed2:792487936272367648><:AquaCollapsed3:792487936829816863>",
        value=Song["score"],
        inline=False
    )
    if Song["pp"] == 0:
        message.add_field(
            name="PP <a:BurgerChamp1:792487936703725600><a:BurgerChamp2:792487936280756246><a:BurgerChamp3:792487936679215134><a:BurgerChamp4:792487936771489832>",
            value="Unranked",
            inline=False
    )
    else:
        message.add_field(
            name="PP <a:BurgerChamp1:792487936703725600><a:BurgerChamp2:792487936280756246><a:BurgerChamp3:792487936679215134><a:BurgerChamp4:792487936771489832>",
            value=round(Song["pp"],2),
            inline=False
    )
        message.add_field(
            name="Weighted PP ⚖️<a:BurgerChamp1:792487936703725600><a:BurgerChamp2:792487936280756246><a:BurgerChamp3:792487936679215134><a:BurgerChamp4:792487936771489832>",
            value=round((Song["weight"] * Song["pp"]),2),
            inline=False
    )
    message.add_field(name="Time Set 🕕🕘", value=(Song["timeSet"])[:10], inline=False)
    message.set_image(url="https://new.scoresaber.com/api/static/covers/" + Song["songHash"] + ".png")
    await ctx.send(embed=message)
    logging.info("embed message sent")


async def songsEmbed(self, ctx, arg_page, arg_user, type):
    if arg_user is not None:
        ctx.author = await userID(self, arg_user)
        logging.info(f"Argument given, now {ctx.author.name}")
    if ctx.author is None:
        logging.info("ctx.author is None")
        return await ctx.send("Sorry Senpai, I can't find anyone with that ID qwq")
    ref = dab.collection("users").document(str(ctx.author.id)).get()
    scoresaber = ref.get('scoresaber')
    if scoresaber is None:
        await ctx.send("Sorry Senpai, that user isn't in my database!")
        return logging.info("scoresaber is None\n----------")
    SS_id = scoresaber[25:]
    if type == "recentSongs":
        URL = (f"https://new.scoresaber.com/api/player/{SS_id}/scores/recent/{arg_page}")
        requestType = ("Recent Songs")
    elif type == "topSongs":
        URL = (f"https://new.scoresaber.com/api/player/{SS_id}/scores/top/{arg_page}")
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
    json_data = json.loads(requests.get(URL1, headers=header).text)
    playerInfo = json_data["playerInfo"]
    songsMessage = ""
    count = 0
    while count != len(songsList):
        Song = songsList[count]
        if Song["songSubName"] == '':
            songTitle = Song["songName"]
        else:
            songTitle = Song["songName"]+" - "+Song["songSubName"]
        songScore = Song["score"]
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
            f"```Song: {songTitle}, "+Song["songAuthorName"]+" - "+Song["levelAuthorName"]+f" ({difficulty})\nRank: #"+str(Song["rank"])+f"\nAcc: {songAcc}%\nScore: {songScore}\nPP: {songPP}\nWeighted PP: {songWeightedPP}\nTime Set: "+(Song["timeSet"])[:10]+"```")
        songsMessage = songsMessage + songMessage
        count = count + 1
    message = discord.Embed(
        title=playerInfo["playerName"]+f"'s {requestType}",
        url=scoresaber,
        description=songsMessage,
        colour=0xffdc1b,
        timestamp=ctx.message.created_at
    )
    await ctx.send(embed=message)
    logging.info("embed message sent")


class scoresaber(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=["ss"])
    async def scoresaber(self, ctx, argument1=None):
        logging.info(f"Recieved >scoresaber {ctx.author.name}")
        if argument1 is not None:
            ctx.author = await userID(self, argument1)
            if ctx.author is None:
                return await ctx.send("Sorry Senpai, I can't find anyone with that ID qwq")
            logging.info(f"Argument given, now {ctx.author.name}")
        async with ctx.channel.typing():
            ref = dab.collection("users").document(str(ctx.author.id)).get()
            scoresaber = ref.get('scoresaber')
            if scoresaber is None:
                await ctx.send("Sorry Senpai, that user isn't in my database!")
                return logging.info("scoresaber is None\n----------")
            SS_id = scoresaber[25:]
            URL = (f"https://new.scoresaber.com/api/player/{SS_id}/full")
            logging.info(URL)
            response = requests.get(URL, headers=header)
            json_data = json.loads(response.text)
            if "error" in json_data:
                return await ctx.send("Uh Oh, the codie wodie did an oopsie! uwu\nCheck if your ScoreSaber link is valid <:AYAYASmile:789578607688417310>")
            playerInfo = json_data["playerInfo"]
            scoreStats = json_data["scoreStats"]
            embed = discord.Embed(
                title=playerInfo["playerName"]+"'s ScoreSaber Stats <:WidePeepoHappy1:757948845362511992><:WidePeepoHappy2:757948845404585984><:WidePeepoHappy3:757948845400522812><:WidePeepoHappy4:757948845463306310>",
                url=scoresaber,
                colour=0xffdc1b,
                timestamp=ctx.message.created_at
            )
            embed.add_field(
                name="Global Rank 🌐",
                value=playerInfo["rank"],
                inline=True
            )
            embed.add_field(
                name=f"Country Rank :flag_"+playerInfo["country"].lower()+":",
                value=playerInfo["countryRank"],
                inline=True
            )
            embed.add_field(
                name="PP <a:PogLick:792002791828357131>",
                value=playerInfo["pp"],
                inline=True
            )
            embed.add_field(
                name="Ranked Acc <:PeepoAcc:792385194351001610>",
                value=str(round(scoreStats["averageRankedAccuracy"], 2))+"%",
                inline=True
            )
            embed.add_field(
                name="Total Play Count <a:ppJedi:754632378206388315>",
                value=scoreStats["totalPlayCount"],
                inline=True
            )
            embed.add_field(
                name="Ranked Play Count 🧑‍🌾",
                value=scoreStats["rankedPlayCount"],
                inline=True
            )
            embed.set_thumbnail(
                url="https://new.scoresaber.com" + playerInfo["avatar"]
            )
        await ctx.send(embed=embed)
        logging.info("Response: ScoreSaber UserData embed\n----------")

    @scoresaber.command(aliases=["rs"])
    async def recentsong(self, ctx, argument1=None, argument2=None):
        logging.info(f"Recieved >scoresaber recentsong {ctx.author.name}")
        async with ctx.channel.typing():
            await songEmbed(self, ctx, argument1, argument2, type="recentSong")
        logging.info("Finished\n----------")

    @scoresaber.command(aliases=["ts"])
    async def topsong(self, ctx, argument1=1, argument2=None):
        logging.info(f"Recieved >scoresaber topsong {ctx.author.name}")
        async with ctx.channel.typing():
            await songEmbed(self, ctx, argument1, argument2, type="topSong")
        logging.info("Finished\n----------")

    @scoresaber.command(aliases=["rss"])
    async def recentsongs(self, ctx, argument1=1, argument2=None):
        logging.info(f"Recieved >scoresaber recentSongs {ctx.author.name}")
        async with ctx.channel.typing():
            await songsEmbed(self, ctx, argument1, argument2, type="recentSongs")
        logging.info("Response: ScoreSaber recentSongs embed\n----------")

    @scoresaber.command(aliases=["tss"])
    async def topsongs(self, ctx, argument1=1, argument2=None):
        logging.info(f"Recieved >scoresaber topSongs {ctx.author.name}")
        async with ctx.channel.typing():
            await songsEmbed(self, ctx, argument1, argument2, type="topSongs")
        logging.info("Response: ScoreSaber topSongs embed\n----------")

    @scoresaber.command(aliases=["com"])
    async def compare(self, ctx, argument1=None, argument2=None):
        if argument1 is None:
            return await ctx.send("You need to mention someone for me to compare you against!")
        elif argument1 is not None and argument2 is not None:
            argument1 = await userID(self, argument1)
            if argument1 is None:
                return await ctx.send("Sorry Senpai, I can't find the first user qwq")
            argument2 = await userID(self, argument2)
            if argument2 is None:
                return await ctx.send("Sorry Senpai, I can't find the second user qwq")
        elif argument1 is not None and argument2 is None:
            argument2 = await userID(self, argument1)
            argument1 = ctx.author
            if argument2 is None:
                return await ctx.send("Sorry Senpai, I can't find anyone with that ID qwq")
        async with ctx.channel.typing():
            user1 = dab.collection("users").document(str(argument1.id)).get()
            user2 = dab.collection("users").document(str(argument2.id)).get()
            scoresaber1 = user1.get('scoresaber')
            scoresaber2 = user2.get('scoresaber')
            if scoresaber1 is None or scoresaber2 is None:
                await ctx.send("Sorry Senpai, that user isn't in my database!")
                return logging.info("scoresaber is None\n----------")
            SS_id1 = scoresaber1[25:]
            SS_id2 = scoresaber2[25:]
        URL1 = (f"https://new.scoresaber.com/api/player/{SS_id1}/full")
        URL2 = (f"https://new.scoresaber.com/api/player/{SS_id2}/full")
        logging.info(f"{URL1}\n{URL2}")
        response1 = requests.get(URL1, headers=header)
        response2 = requests.get(URL2, headers=header)
        json_data1 = json.loads(response1.text)
        json_data2 = json.loads(response2.text)
        if "error" in json_data1 or "error" in json_data2:
            return await ctx.send("Uh Oh, the codie wodie did an oopsie! uwu\nCheck if both user's ScoreSaber links are valid <:AYAYASmile:789578607688417310>")
        playerInfo1 = json_data1["playerInfo"]
        scoreStats1 = json_data1["scoreStats"]
        playerInfo2 = json_data2["playerInfo"]
        scoreStats2 = json_data2["scoreStats"]
        val1 = int(playerInfo1["rank"])
        val2 = int(playerInfo2["rank"])
        if val1 < val2:
            val1 = f"__{val1}__"
        elif val1 > val2:
            val2 = f"__{val2}__"
        message = f"{val1} - 🌐 **Global Rank** 🌐 - {val2}\n"
        val1 = int(playerInfo1["countryRank"])
        val2 = int(playerInfo2["countryRank"])
        if val1 < val2:
            val1 = f"__{val1}__"
        elif val1 > val2:
            val2 = f"__{val2}__"
        message = message + f"{val1} - :flag_"+playerInfo1["country"].lower()+": **Country Rank** :flag_"+playerInfo2["country"].lower()+f": - {val2}\n"
        val1 = int(playerInfo1["pp"])
        val2 = int(playerInfo2["pp"])
        if val1 < val2:
            val1 = f"__{val1}__"
        elif val1 > val2:
            val2 = f"__{val2}__"
        message = message + f"{val1} - <a:PogLick:792002791828357131> **Performance Points** <a:PogLick:792002791828357131> - {val2}\n"
        val1 = float(round(scoreStats2["averageRankedAccuracy"], 2))
        val2 = float(round(scoreStats1["averageRankedAccuracy"], 2))
        if val1 < val2:
            val1 = f"__{val1}__"
        elif val1 > val2:
            val2 = f"__{val2}__"
        message = message + f"{val1}% - <:PeepoAcc:792385194351001610> **Ranked Acc** <:PeepoAcc:792385194351001610> - {val2}%\n"
        val1 = int(scoreStats1["totalPlayCount"])
        val2 = int(scoreStats2["totalPlayCount"])
        if val1 < val2:
            val1 = f"__{val1}__"
        elif val1 > val2:
            val2 = f"__{val2}__"
        message = message + f"{val1} -  <a:ppJedi:754632378206388315> **Total Play Count**  <a:ppJedi:754632378206388315> - {val2}\n"
        val1 = int(scoreStats1["rankedPlayCount"])
        val2 = int(scoreStats2["rankedPlayCount"])
        if val1 < val2:
            val1 = f"__{val1}__"
        elif val1 > val2:
            val2 = f"__{val2}__"
        message = message + f"{val1} -  🧑‍🌾 **Ranked Play Count**  🧑‍🌾 - {val2}\n"
        embed = discord.Embed(
            title=playerInfo1["playerName"]+" 🆚 "+playerInfo2["playerName"],
            description=message,
            colour=0xffdc1b,
            timestamp=ctx.message.created_at
        )
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(scoresaber(client))
