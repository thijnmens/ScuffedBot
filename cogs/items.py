import logging
import asyncio
from discord.ext import commands
from discord.utils import get
from firebase_admin import firestore
from random import randint

dab = firestore.client()

class items(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True)
    @commands.cooldown(1, 600, commands.BucketType.user)
    async def use(self, ctx, argument=None):
        logging.info('Recieved: >use')
        await ctx.send('What do you want to use senpai?')
        logging.info('Response: missing arguments\n----------')
    
    @use.group(aliases=["gun"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def use_gun(self, ctx):
        logging.info('Recieved: >use gun')
        inv = dab.collection('users').document(str(ctx.author.id)).get().get('inv')
        inv_len = len(inv)
        a = 0
        hasitem = False
        while a < inv_len:
            item = str(inv[a]).split('~')
            if item[0] == 'gun' and int(item[1]) > 0:
                hasitem = True
            a = a + 1
        if hasitem == True:
            try:
                sent = await ctx.send('Who do you want to use the gun on?')
                msg = await self.bot.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
                user = str(msg.content)
                if '@' in user:
                    user = user.replace('<', '')
                    user = user.replace('@', '')
                    user = user.replace('!', '')
                    user = user.replace('>', '')
            except asyncio.TimeoutError:
                await sent.delete()
                return await ctx.send("You didn't reply in time, please restart the process")
            if(str(user) == str(ctx.author.id)):
                await ctx.send('WAIT SENPAI, DON\'T DO IT!')
            else:
                bala = int(dab.collection('users').document(str(ctx.author.id)).get().get('bal'))
                balb = int(dab.collection('users').document(str(user)).get().get('bal'))
                rand = randint(1, 10)
                a = str(ctx.guild.get_member(int(ctx.author.id))).split('#')
                b = str(ctx.guild.get_member(int(user))).split('#')
                if rand <= 3:
                    inv = dab.collection('users').document(str(ctx.author.id)).get().get('inv')
                    money = randint(0, (round(bala/2, 0)))
                    inv_len = len(inv)
                    c = 0
                    while c < inv_len:
                        item = str(inv[c]).split('~')
                        if item[0] == 'gun':
                            count = int(item[1]) - 1
                            inv[c] = f'gun~{count}'
                            dab.collection('users').document(str(ctx.author.id)).update({'inv': inv})
                        c = c + 1
                    bala = bala - money
                    balb = balb + money
                    dab.collection('users').document(str(ctx.author.id)).update({'bal': bala})
                    dab.collection('users').document(str(user)).update({'bal': balb})
                    dab.collection('users').document(str(ctx.author.id)).update({'inv': inv})
                    await ctx.send(f'{a[0]} tried to kill {b[0]} with a gun, but they missed and {a[0]} was arrested\n{b[0]} earned {money} coins and {a[0]} lost their gun')
                    logging.info(f'Response: {ctx.author.id} tried to kill {user}\n----------')
                else:
                    money = randint(0, (round(balb/2, 0)))
                    bala = bala + money
                    balb = balb - money
                    dab.collection('users').document(str(ctx.author.id)).update({'bal': bala})
                    dab.collection('users').document(str(user)).update({'bal': balb})
                    await ctx.send(f'{a[0]} killed {b[0]} using a gun\n{a[0]} found {money} coins in their wallet')
                    logging.info(f'Response: {ctx.author.id} killed {user}\n----------')
        else:
            await ctx.send('How are you going to use it if you don\'t even own it?')
            logging.info('Response: no gun in inv\n----------')

def setup(bot):
    bot.add_cog(items(bot))