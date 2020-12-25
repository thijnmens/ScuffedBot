import discord, os, requests, json, firebase_admin, asyncio
from datetime import datetime
from discord.ext import commands
from discord.utils import get
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
dab = firestore.client()

class BirthdayCheck(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Check for birthdays
    def get_birthdays(self, ctx):
        try:
            ref = dab.collection('collectionlist').document('data').get().get('collectionarray')
            amount = len(ref) - 1
        except Exception as e:
            print(e)

    #Test
    @commands.command()
    async def test(self, ctx):
        print('Recieved: >test')
        print(current_time)
        await ctx.send('testing complete')
        print('Response: testing complete')
        print('----------')

def setup(client):
    client.add_cog(BirthdayCheck(client))