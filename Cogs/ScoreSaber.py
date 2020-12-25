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

    @commands.command()
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
        print (response.text)
        json_data = json.loads(response.text)
        playerInfo = json_data["playerInfo"]
        playerCountry = playerInfo["country"]
        playerName = playerInfo["playerName"]
        embed=discord.Embed(
            title = f"{playerName}'s ScoreSaber Stats",
            colour = 0xffdc1b
        )
        embed.add_field(name="Global Rank", value=playerInfo["rank"], inline=False)
        embed.add_field(name=f"Country Rank ({playerCountry})", value=playerInfo["countryRank"], inline=False)
        embed.add_field(name="PP <a:PogLick:792002791828357131>", value=playerInfo["pp"], inline=True)
        embed.set_thumbnail(url="https://new.scoresaber.com"+playerInfo["avatar"])
        await ctx.send(embed=embed)
        print ("Response: ScoreSaber UserData embed")
        print('----------')

def setup(client):    
    client.add_cog(ScoreSaber(client))