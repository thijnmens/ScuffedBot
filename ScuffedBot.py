#########################
#      Scuffed Bot      #
#########################
# Created by: Thijnmens #
#    Version: 1.0.0     #
#########################

import discord, os
from discord.ext import commands
from discord.utils import get

intents = discord.Intents.default()
client = commands.Bot(command_prefix=">", intents=intents, case_insensitive=True)
client.remove_command('help')
cwd = os.getcwd()
            
try: #literally copy and pasted this from one of my discord bots lol
    for filename in os.listdir(f'{cwd}/Cogs/'): #Heroku weird
        if filename.endswith(".py"):
           client.load_extension(f"Cogs.{filename[:-3]}")
except Exception as e:
    print(f"Possible fatal error:\n{e}\nThis means that the cogs have not started correctly!")

#Bot Startup
@client.event
async def on_ready():
    print('Bot has successfully launched as {0.user}'.format(client))

#Login to discord   
client.run(os.getenv("TOKEN"))