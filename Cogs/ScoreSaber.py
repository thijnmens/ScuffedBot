import discord, os, requests, json, firebase_admin
from discord.ext import commands
from discord.utils import get
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db

cred = credentials.Certificate({
  "type": "service_account",
  "project_id": os.getenv("PROJECT_ID").replace('\\n', '\n'),
  "private_key_id": os.getenv("PRIVATE_KEY_ID").replace('\\n', '\n'),
  "private_key": os.getenv("PRIVATE_KEY").replace('\\n', '\n'),
  "client_email": os.getenv("CLIENT_EMAIL").replace('\\n', '\n'),
  "client_id": os.getenv("CLIENT_ID").replace('\\n', '\n'),
  "auth_uri": os.getenv("AUTH_URI").replace('\\n', '\n'),
  "token_uri": os.getenv("TOKEN_URI").replace('\\n', '\n'),
  "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL").replace('\\n', '\n'),
  "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL").replace('\\n', '\n')
  })
default_app = firebase_admin.initialize_app(cred)
dab = firestore.client()

SS_id = None
page = int(0)
URL1 = (f"https://new.scoresaber.com/api/player/{SS_id}/full") #Get UserData
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
            SS_id = argument1[26:]
            print (SS_id)
        else: 
            ref = dab.collection(str(ctx.author.id)).document('data').get()
            scoresaber = ref.get('scoresaber')
            SS_id = scoresaber[26:]
            print (SS_id)
        response = requests.get(URL1)
        print (response)
        #do flashy json shit here and output something

def setup(client):    
    client.add_cog(ScoreSaber(client))