from logging import basicConfig, INFO, info as logging_info, error as logging_error
from os import getcwd, getenv

from discord import Intents, AllowedMentions
from firebase_admin import credentials, initialize_app
from dotenv import load_dotenv

from discord.ext import commands
from utils import jskp


basicConfig(format='%(levelname)s: %(message)s', level=INFO)

cwd = getcwd()
load_dotenv(f"{cwd}/config.env")

intents = Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=">", help_command=None, intents=intents, case_insensitive=True, allowed_mentions=AllowedMentions(replied_user=False))


cred = credentials.Certificate({
    "type": "service_account",
    "project_id": "scuffed-bot",
    "private_key_id": "0a9e4df141fc09de72b6d06bebf416adef1f2227",
    "private_key": getenv("PRIVATE_KEY").replace('\\n', '\n'),
    "client_email": "firebase-adminsdk-cudqh@scuffed-bot.iam.gserviceaccount.com",
    "client_id": "116271581448704145426",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-cudqh%40scuffed-bot.iam.gserviceaccount.com"
    })
default_app = initialize_app(cred)

initial_cogs = [
    "jishaku",
    "cogs.birthday_check",
    "cogs.challonge",
    "cogs.coord",
    "cogs.database",
    "cogs.economy",
    "cogs.error_handler",
    "cogs.general",
    "cogs.help",
    "cogs.items",
    "cogs.neko",
    "cogs.nhentai",
    "cogs.scoresaber",
    "cogs.status",
    "cogs.tourn_app",
    "cogs.user",
    "cogs.work"
]

for cog in initial_cogs:
    try:
        bot.load_extension(cog)
        logging_info(f"Successfully loaded {cog}")
    except Exception as e:
        logging_error(f"Failed to load cog {cog}: {e}")


# Bot Startup
@bot.event
async def on_ready():
    logging_info(f'Bot has successfully launched as {bot.user}')

@bot.before_invoke
async def before_invoke(ctx):
    logging_info(f"""------------------------------
Invoked {ctx.command} in {ctx.guild.name} by {ctx.author.name}\nArgs: {ctx.args}""")

@bot.after_invoke
async def after_invoke(ctx):
    logging_info(f"Concluded {ctx.command}")

# Login to discord
bot.run(getenv("TOKEN"))
