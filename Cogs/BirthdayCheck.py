import discord, os, requests, json, firebase_admin, asyncio, schedule
from datetime import datetime
from discord.ext import commands, tasks
from discord.utils import get
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db

now = datetime.now()
current_time = now.strftime("%Y-%m-%d-%H")
dab = firestore.client()
check = False

class BirthdayCheck(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    def cog_unload(self):
        self.loop.cancel()

    @commands.Cog.listener()
    async def on_ready(self):
        print("BirthdayCheck cog loaded")
    
    #Check for birthdays
    async def get_birthdays(self, ctx):
        try:
            ref = dab.collection('collectionlist').document('data').get().get('collectionarray')
            amount = len(ref) - 1
        except Exception as e:
            print(e)

    async def countdown(self, ctx):
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d-%H")
        try:
            if current_time == '2020-12-25-16':
                channel = client.get_channel(754627439413690469)
                await channel.send('3 More Days till a̶̧͔̱̰̩̋͑̅̾͗̈́̐͂̚͘g̸̺̣̟̜̓̓́́͘h̸͖͈̺̿̊͆͒̅̎̑̚ͅa̴̙̫̗̟͐͂̈̀̒̅͛̉͠s̴̺̔̌͑͑s̷̞̥͈͚̺͈͕̀̀͂̇́͘ͅȁ̵̬̀̂̂̎͝g̸͓̞̑̐̏̉́͆͝h̷̹̯̣͈̻̺͑̾́́̔͗̐̓͘k̸̯̟̼̮̜̏͐͜....')
            if current_time == '2020-12-26-16':
                channel = client.get_channel(754627439413690469)
                await channel.send('2 More Days till a̶̧͔̱̰̩̋͑̅̾͗̈́̐͂̚͘g̸̺̣̟̜̓̓́́͘h̸͖͈̺̿̊͆͒̅̎̑̚ͅa̴̙̫̗̟͐͂̈̀̒̅͛̉͠s̴̺̔̌͑͑s̷̞̥͈͚̺͈͕̀̀͂̇́͘ͅȁ̵̬̀̂̂̎͝g̸͓̞̑̐̏̉́͆͝h̷̹̯̣͈̻̺͑̾́́̔͗̐̓͘k̸̯̟̼̮̜̏͐͜....')
            if current_time == '2020-12-27-16':
                channel = client.get_channel(754627439413690469)
                await channel.send('1 More Day till a̶̧͔̱̰̩̋͑̅̾͗̈́̐͂̚͘g̸̺̣̟̜̓̓́́͘h̸͖͈̺̿̊͆͒̅̎̑̚ͅa̴̙̫̗̟͐͂̈̀̒̅͛̉͠s̴̺̔̌͑͑s̷̞̥͈͚̺͈͕̀̀͂̇́͘ͅȁ̵̬̀̂̂̎͝g̸͓̞̑̐̏̉́͆͝h̷̹̯̣͈̻̺͑̾́́̔͗̐̓͘k̸̯̟̼̮̜̏͐͜....')
        except Exception as e:
            print(e)

    schedule.every().day.at("16:50").do(countdown)

    #Test
    @commands.command()
    async def test(self, ctx):
        print('Recieved: >test')
        print(current_time)
        await ctx.send('testing complete')
        print('Response: testing complete')
        print('----------')

    #Infinite Loop
    @tasks.loop(minute=1)
    async def checker(self, ctx):
        print('something')
        schedule.run_pending()
        
    checker.start()

def setup(client):
    client.add_cog(BirthdayCheck(client))