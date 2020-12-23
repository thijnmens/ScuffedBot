#########################
#      Scuffed Bot      #
#########################
# Created by: Thijnmens #
#    Version: 1.0.0     #
#########################

import discord, os, logging
from discord.ext import commands
from discord.utils import get

intents = discord.Intents.default()
client = commands.Bot(command_prefix=">", intents=intents, case_insensitive=True)
client.remove_command('help')
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s: %(message)s',level=logging.INFO)
cwd = os.getcwd()
            
try: #literally copy and pasted this from one of my discord bots lol
    for filename in os.listdir(f'{cwd}/Cogs/'): #Heroku weird
        if filename.endswith(".py"):
           client.load_extension(f"Cogs.{filename[:-3]}")
except Exception as e:
    logging.critical(f"Possible fatal error:\n{e}\nThis means that the cogs have not started correctly!")

#Bot Startup
@client.event
async def on_ready():
    logging.info('Bot has successfully launched as {0.user}'.format(client))

#Login to discord   
client.run(os.getenv("TOKEN"))