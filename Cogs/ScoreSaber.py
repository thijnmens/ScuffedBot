import discord, os, requests, json, firebase_admin
from discord.ext import commands
from discord.utils import get
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db

dab = firestore.client()

SS_id = None
page = int(0)
#https://new.scoresaber.com/api/player/76561198091128855/full
#https://new.scoresaber.com/api/static/covers/69E494F4A295197BF03720029086FABE6856FBCE.png
#URL = (f"https://new.scoresaber.com/api/player/{SS_id}/full") - Get UserData
#URL = (f"https://new.scoresaber.com/api/player/{SS_id}/scores/top/{page}") - #Get Top Songs
#URL = (f"https://new.scoresaber.com/api/player/{SS_id}/scores/recent/{page}") - #Get Recent Songs
#URL = (f"https://new.scoresaber.com/api/players/{page}") - #Get Global Rankings
#URL = (f"https://new.scoresaber.com/api/players/pages") - #Get Global Ranking Pages

class ScoreSaber(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("ScoreSaber cog loaded")
 
    @commands.group(invoke_without_command=True)
    async def scoresaber(self, ctx, argument1=None):
        print (f"Recieved >scoresaber {ctx.author.name}")
        if argument1 is not None:
            ID = argument1[3:]
            ID = ID[:-1]
            ctx.author = self.client.get_user(int(ID))
            print (f"Argument given, now {ctx.author.name}")
        ref = dab.collection(str(ctx.author.id)).document('data').get()
        scoresaber = ref.get('scoresaber')
        SS_id = scoresaber[25:]
        URL = (f"https://new.scoresaber.com/api/player/{SS_id}/full")
        print (URL)
        response = requests.get(URL)
        json_data = json.loads(response.text)
        playerInfo = json_data["playerInfo"]
        scoreStats = json_data["scoreStats"]
        playerCountry = playerInfo["country"]
        playerName = playerInfo["playerName"]
        playerCountryFlag = (f":flag_{playerCountry.lower()}:")
        embed=discord.Embed(
            title = f"[{playerName}'s]({scoresaber}) ScoreSaber Stats <:WidePeepoHappy1:757948845362511992><:WidePeepoHappy2:757948845404585984><:WidePeepoHappy3:757948845400522812><:WidePeepoHappy4:757948845463306310>",
            colour = 0xffdc1b,
            timestamp = ctx.message.created_at
        )
        embed.add_field(name="Global Rank 🌐", value=playerInfo["rank"], inline=True)
        embed.add_field(name=f"Country Rank {playerCountryFlag}", value=playerInfo["countryRank"], inline=True)
        embed.add_field(name="PP <a:PogLick:792002791828357131>", value=playerInfo["pp"], inline=True)
        embed.add_field(name="Ranked Acc <:PeepoAcc:792385194351001610>", value=round(scoreStats["averageRankedAccuracy"], 2), inline=True)
        embed.add_field(name="Total Play Count <a:ppJedi:754632378206388315>", value=scoreStats["totalPlayCount"], inline=True)
        embed.add_field(name="Ranked Play Count 🧑‍🌾", value=scoreStats["rankedPlayCount"], inline=True)
        embed.set_thumbnail(url="https://new.scoresaber.com"+playerInfo["avatar"])
        await ctx.send(embed=embed)
        print ("Response: ScoreSaber UserData embed")
        print('----------')

    @scoresaber.command()
    async def recentsong(self, ctx, argument1=None):
        print (f"Recieved >scoresaber recentsong {ctx.author.name}")
        if argument1 is not None:
            ID = argument1[3:]
            ID = ID[:-1]
            ctx.author = self.client.get_user(int(ID))
            print (f"Argument given, now {ctx.author.name}")
        ref = dab.collection(str(ctx.author.id)).document('data').get()
        scoresaber = ref.get('scoresaber')
        SS_id = scoresaber[25:]
        URL = (f"https://new.scoresaber.com/api/player/{SS_id}/scores/recent")
        URL1 = (f"https://new.scoresaber.com/api/player/{SS_id}/full")
        print (URL)
        print (URL1)
        response = requests.get(URL)
        json_data = json.loads(response.text)
        recentSongs = json_data["scores"]
        response = requests.get(URL1)
        json_data = json.loads(response.text)
        playerInfo = json_data["playerInfo"]
        playerName = playerInfo["playerName"]
        recentSong = recentSongs[0]
        songName = recentSong["songName"]
        songSubName = recentSong["songSubName"]
        embed=discord.Embed(
            title = f"{songName} - {songSubName}",
            description = recentSong["songAuthorName"],
            colour = 0xffdc1b,
            timestamp = ctx.message.created_at
        )
        embed.set_author(name=playerName, url=scoresaber, icon_url="https://new.scoresaber.com"+playerInfo["avatar"])
        embed.add_field(name="Song Diff", value="a")
        embed.add_field(name="Rank", value=recentSong["rank"], inline=True)
        embed.add_field(name="Score", value=recentSong["score"], inline=True)
        embed.add_field(name="PP", value=recentSong["pp"], inline=True)
        embed.set_thumbnail(url="https://new.scoresaber.com/api/static/covers/"+recentSong["songHash"]+".png")
        await ctx.send(embed=embed)
        print ("Response: ScoreSaber RecentSong embed")
        print('----------')

def setup(client):    
    client.add_cog(ScoreSaber(client))