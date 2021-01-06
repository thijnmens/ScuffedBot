import discord, os, requests, json, firebase_admin, asyncio
from datetime import datetime
from discord.ext import commands, tasks
from discord.utils import get
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db

client = discord.Client()
now = datetime.now()
current_time = now.strftime("%d-%m")
dab = firestore.client()
check = False

class BirthdayCheck(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.infinite_loop.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print("BirthdayCheck cog loaded")
    
    @birthday.command()
    #Check for birthdays
    async def get_birthdays(self, ctx):
        try:
            ref = dab.collection('collectionlist').document('data').get().get('collectionarray')
            amount = len(ref)
            count = 0
            while(count < amount):
                ID = ref[count]
                print(ID)
                birthday = dab.collection(str(ID)).document('data').get().get('birthday')
                print(birthday)
                birthdaysplit = birthday.split('/')
                print(birthdaysplit)
                birthdayfinal = birthdaysplit[0] + '-' + birthdaysplit[1]
                print(birthdayfinal)
                current_time = now.strftime("%d-%m")
                print(current_time)
                a = dab.collection(str(ID)).document('data').get().get('a')
                print(a)
                if(birthdayfinal == current_time & a == False):
                    channel = client.get_channel(793049781554642954)
                    await channel.send(f'<:HyperTada:796323264888307731> Happy birtday <!@{ID}>! <:HyperTada:796323264888307731>')
                    print(f'Wished {ID} a happy birthday')
                    a = dab.collection(str(ID)).document('data').update({'a':True})
        except Exception as e:
            print(e)

    #Test
    @commands.command()
    async def test(self, ctx):
        print('Recieved: >test')
        ###VVV testing here VVV###
        get_birthdays()
        ###^^^ testing here ^^^###
        await ctx.send('testing complete')
        print('Response: testing complete')
        print('----------')

def setup(client):
    client.add_cog(BirthdayCheck(client))