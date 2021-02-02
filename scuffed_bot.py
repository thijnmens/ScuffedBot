#########################
#      Scuffed Bot      #
#########################
# Created by: Thijnmens #
#    Version: 1.0.0     #
#########################

import discord
import os
import logging
import firebase_admin
from random import randint
from discord.ext import commands, tasks
from discord.utils import get
from firebase_admin import credentials

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=">",intents=intents,case_insensitive=True,allowed_mentions=discord.AllowedMentions(replied_user=False))
client.remove_command('help')
cwd = os.getcwd()
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
funniList = [
    "Aso kinda cute 😳",
    "I'm wowking vewy hawd!! uwu",
    "Grinding PP",
    "Doin' ur mom",
    "Do >NOPE",
    "Hi cutie owo",
    "Scuffed Saber",
    "Scuffed Walls",
    "01101000 01101001",
    "Scuffing your mum",
    "My sister is a dumbass",
    "Shiny Happy Days"]

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

initial_cogs = [
    "cogs.dev",
    "cogs.error_handler",
    #"cogs.chain_enforcement",
    "cogs.challonge",
    "cogs.birthday_check",
    "cogs.help",
    "cogs.scoresaber",
    "cogs.text",
    "cogs.tourn_app",
    "cogs.neko",
    "cogs.nhentai",
    "cogs.user"
]

for cog in initial_cogs:
    try:
        client.load_extension(cog)
        logging.info(f"Successfully loaded {cog}")
    except Exception as e:
        logging.error(f"Failed to load cog {cog}: {e}")


@tasks.loop(hours=1)
async def status():
    value = randint(0, len(funniList))
    value = value - 1
    await client.change_presence(activity=discord.Game(name=funniList[value]))
    logging.info(f"Status set to: {funniList[value]}")

# Bot Startup
@client.event
async def on_ready():
    logging.info('Bot has successfully launched as {0.user}'.format(client))
    status.start()

# Login to discord
client.run(os.getenv("TOKEN"))
