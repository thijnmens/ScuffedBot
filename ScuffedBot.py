#########################
#      Scuffed Bot      #
#########################
# Created by: Thijnmens #
#    Version: 1.0.0     #
#########################

import discord, os, firebase_admin
from random import randint
from discord.ext import commands, tasks
from discord.utils import get
from firebase_admin import credentials

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=">", intents=intents, case_insensitive=True)
client.remove_command('help')
client.allowed_mentions(replied_user=False)
cwd = os.getcwd()
funniList = ["Join the NOPE clan", "Aso kinda cute 😳", "I'm wowking vewy hawd!! uwu", "Grinding PP", "Doin' ur mom", "Scuffed code goes brrr", "Do >NOPE", "Hi cutie owo", "Scuffed Saber","Scuffed Walls","Shiny Happy Days"]

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

try: #literally copy and pasted this from one of my discord bots lol
    for filename in os.listdir(f'{cwd}/Cogs/'): #Heroku weird
        if filename.endswith(".py"):
           client.load_extension(f"Cogs.{filename[:-3]}")
except Exception as e:
    print(f"Possible fatal error:\n{e}\nThis means that the cogs have not started correctly!")

@tasks.loop(hours=1)
async def status():
    value = randint(0,len(funniList))
    value = value - 1
    await client.change_presence(activity=discord.Game(name=funniList[value]))
    print (f"Status set to: {funniList[value]}")

#Bot Startup
@client.event
async def on_ready():
    print('Bot has successfully launched as {0.user}'.format(client))
    status.start()

#Login to discord   
client.run(os.getenv("TOKEN"))