from logging import info as logging_info
from random import randint

from firebase_admin import firestore

from discord.ext import commands

dab = firestore.client()

class work(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(invoke_without_command=True, )
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def work(self, ctx):
        try:
            job = dab.collection('users').document(str(ctx.author.id)).get().get('job')
        except:
            job = False
        if job is True:
            pro = randint(0, 666)
            bal = dab.collection('users').document(str(ctx.author.id)).get().get('bal')
            bal = bal + pro
            dab.collection('users').document(str(ctx.author.id)).update({'bal': bal})
            await ctx.send(f'WOW! You made a whole {pro} coins!')
            logging_info(f'Response: user {ctx.author.id} has earned {pro}, their total is {bal}\n----------')
        else:
            await ctx.send('You should get a job first senpai! try >job get')
    
    @commands.group(invoke_without_command=True, )
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def job(self, ctx):
        try:
            job = dab.collection('users').document(str(ctx.author.id)).get().get('job')
        except:
            job = False
        if job is True:
            jtype = dab.collection('users').document(str(ctx.author.id)).get().get('jtype')
            await ctx.send(f'You are currently working as a {jtype}! I\'m so proud of you senpai UwU')
            logging_info(f'Response: job is {jtype}\n----------')
        else:
            await ctx.send('You should get a job first senpai!')
        
    @job.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def get(self, ctx):
        try:
            job = dab.collection('users').document(str(ctx.author.id)).get().get('job')
        except:
            job = False
        if job is False:
            dab.collection('users').document(str(ctx.author.id)).update({'job': True})
            await ctx.send('You found a job!?! Really! i\'m so proud of you UwU')
        else:
            await ctx.send('You already have a job senpai!')


def setup(bot):
    bot.add_cog(work(bot))