import logging
import asyncio
from discord.ext import commands
from discord.utils import get
from firebase_admin import firestore
from random import randint

dab = firestore.client()

class work(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def work(self, ctx):
        logging.info('Recieved: >work')
        try:
            job = dab.collection('users').document(str(ctx.author.id)).get().get('job')
        except:
            job = False
        if job == True:
            pro = randint(0, 666)
            bal = dab.collection('users').document(str(ctx.author.id)).get().get('bal')
            bal = bal + pro
            dab.collection('users').document(str(ctx.author.id)).update({'bal': bal})
            await ctx.send(f'WOW! You made a whole {pro} coins!')
            logging.info(f'Response: user {ctx.author.id} has earned {pro}, their total is {bal}\n----------')
        else:
            await ctx.send('You should get a job first senpai! try >job get')
            logging.info('Response: no job\n----------')
    
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def job(self, ctx, argument=None):
        if argument == None:
            logging.info('Recieved: >job')
            try:
                job = dab.collection('users').document(str(ctx.author.id)).get().get('job')
            except:
                job = False
            if job == True:
                jtype = dab.collection('users').document(str(ctx.author.id)).get().get('jtype')
                await ctx.send(f'You are currently working as a {jtype}! I\'m so proud of you senpai UwU')
                logging.info(f'Response: job is {jtype}\n----------')
            else:
                await ctx.send('You should get a job first senpai!')
                logging.info('Response: no job\n----------')
        elif argument.lower() == 'get':
            logging.info('Recieved: >job get')
            try:
                job = dab.collection('users').document(str(ctx.author.id)).get().get('job')
            except:
                job = False
            if job == False:
                dab.collection('users').document(str(ctx.author.id)).update({'job': True})
                await ctx.send('You found a job!?! Really! i\'m so proud of you UwU')
                logging.info(f'Response: user {ctx.author.id} now has a job\n----------')
            else:
                await ctx.send('You already have a job senpai!')
                logging.info(f'Response: user {ctx.author.id} already has a job\n----------')
        else:
            await ctx.send('Even i don\'t get what you are trying to do')
            logging.info('Response: missing arguments\n----------')

def setup(client):
    client.add_cog(work(client))