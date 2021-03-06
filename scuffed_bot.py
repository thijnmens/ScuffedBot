import discord
import os
import logging
import firebase_admin
from dotenv import load_dotenv
from random import randint
from discord.ext import commands, tasks
from firebase_admin import credentials
from utils import jskp


cwd = os.getcwd()
load_dotenv(f"{cwd}/config.env")
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=">",intents=intents,case_insensitive=True,allowed_mentions=discord.AllowedMentions(replied_user=False))
bot.remove_command('help')
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

status_list = [
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
    "Shiny Happy Days"
]

cred = credentials.Certificate({
    "type": "service_account",
    "project_id": "scuffed-bot",
    "private_key_id": "0a9e4df141fc09de72b6d06bebf416adef1f2227",
    "private_key": os.getenv("PRIVATE_KEY").replace('\\n', '\n'),
    "client_email": "firebase-adminsdk-cudqh@scuffed-bot.iam.gserviceaccount.com",
    "client_id": "116271581448704145426",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-cudqh%40scuffed-bot.iam.gserviceaccount.com"
    })
default_app = firebase_admin.initialize_app(cred)

initial_cogs = [
    "jishaku",
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
    "cogs.user",
    "cogs.economy",
    "cogs.coord",
    "cogs.items",
    "cogs.work",
    "cogs.database"
]

for cog in initial_cogs:
    try:
        bot.load_extension(cog)
        logging.info(f"Successfully loaded {cog}")
    except Exception as e:
        logging.error(f"Failed to load cog {cog}: {e}")


@tasks.loop(hours=1)
async def status():
    await bot.wait_until_ready()
    value = randint(0, len(status_list))
    value = value - 1
    await bot.change_presence(activity=discord.Game(name=status_list[value]))
    logging.info(f"Status set to: {status_list[value]}")

# Bot Startup
@bot.event
async def on_ready():
    logging.info('Bot has successfully launched as {0.user}'.format(bot))
    status.start()

# Login to discord
bot.run(os.getenv("TOKEN"))
