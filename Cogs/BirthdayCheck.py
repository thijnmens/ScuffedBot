import discord, os, requests, json, firebase_admin, asyncio
from datetime import datetime
from discord.ext import commands
from discord.utils import get
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db

now = datetime.now()
current_time = now.strftime("%Y-%m-%d %H:%M:%S")
dab = firestore.client()

class BirthdayCheck(commands.Cog):
    def __init__(self, client):
        self.client = client

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
        try:
            if current_time == '2020-12-25 16:10:00':
                channel = client.get_channel(754627439413690469)
                await channel.send('3 More Days till a̶̧͔̱̰̩̋͑̅̾͗̈́̐͂̚͘g̸̺̣̟̜̓̓́́͘h̸͖͈̺̿̊͆͒̅̎̑̚ͅa̴̙̫̗̟͐͂̈̀̒̅͛̉͠s̴̺̔̌͑͑s̷̞̥͈͚̺͈͕̀̀͂̇́͘ͅȁ̵̬̀̂̂̎͝g̸͓̞̑̐̏̉́͆͝h̷̹̯̣͈̻̺͑̾́́̔͗̐̓͘k̸̯̟̼̮̜̏͐͜....')
        except Exception as e:
            print(e)

    #Test
    @commands.command()
    async def test(self, ctx):
        print('Recieved: >test')
        print(now)
        get_birthdays()
        await ctx.send('testing complete')
        print('Response: testing complete')
        print('----------')

    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        break

def setup(client):
    client.add_cog(BirthdayCheck(client))