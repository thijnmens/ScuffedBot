import discord, os, requests, json, firebase_admin, asyncio, schedule, time
from discord.ext import commands
from discord.utils import get
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db

dab = firestore.client()
check = False
schedule.every().day.at("12:00").do(get_birthdays) #Not too sure how this works or where it's supposed to go

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
        get_birthdays()
        await ctx.send('testing complete')
        print('Response: testing complete')
        print('----------')


while check == False:
    asyncio.sleep(3600) #Will pause only this while loop for 1 hour
    schedule.run_pending()
    check = True
    break

def setup(client):
    client.add_cog(BirthdayCheck(client))