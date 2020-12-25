import discord, os, requests, json, firebase_admin
from discord.ext import commands
from discord.utils import get
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db

dab = firestore.client()

SS_id = None
page = int(0)
URL1 = (f"https://new.scoresaber.com/api/player/{SS_id}/full") #Get UserData
#https://new.scoresaber.com/api/player/76561198091128855/full
URL2 = (f"https://new.scoresaber.com/api/player/{SS_id}/scores/top/{page}") #Get Top Songs
URL3 = (f"https://new.scoresaber.com/api/player/{SS_id}/scores/recent/{page}") #Get Recent Songs
URL4 = (f"https://new.scoresaber.com/api/players/{page}") #Get Global Rankings
URL5 = (f"https://new.scoresaber.com/api/players/pages") #Get Global Ranking Pages

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
            SS_id = argument1[25:]
            print (SS_id)
        else: 
            ref = dab.collection(str(ctx.author.id)).document('data').get()
            scoresaber = ref.get('scoresaber')
            SS_id = scoresaber[25:]
            print (SS_id)
        print (URL1)
        response = requests.get(URL1)
        print (response)
        json_data = json.loads(response.text)
        print (json_data[0]["playerName"]) #I'm too lazy to see what the value is for
        print (json_data[1]["playerName"]) #this is so I don't have to make multiple commits
        print (json_data[2]["playerName"]) #I'm smart I swear
        print (json_data[3]["playerName"]) #please
        print (json_data[4]["playerName"]) #uwu

def setup(client):    
    client.add_cog(ScoreSaber(client))