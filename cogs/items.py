import asyncio
from random import randint
from logging import info as logging_info

from firebase_admin import firestore

from discord.ext import commands
from discord.utils import get

dab = firestore.client()

class items(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, )
    async def use(self, ctx):
        await ctx.send('What do you want to use senpai?')
        logging_info('Response: missing arguments\n----------')
    
    @use.group(aliases=["gun"])
    @commands.cooldown(1, 600, commands.BucketType.user)
    async def use_gun(self, ctx):
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
                    user = user[3:]
                    user = user[:-1]
            except asyncio.TimeoutError:
                await sent.delete()
                return await ctx.send("You didn't reply in time, please restart the process")
            if(str(user) == str(ctx.author.id)):
                await ctx.send('WAIT SENPAI, DON\'T DO IT!')
            else:
                bala = int(dab.collection('users').document(str(ctx.author.id)).get().get('bal'))
                balb = int(dab.collection('users').document(str(user)).get().get('bal'))
                inv = dab.collection('users').document(str(ctx.author.id)).get().get('inv')
                rand = randint(1, 10)
                a = str(ctx.guild.get_member(int(ctx.author.id))).split('#')
                b = str(ctx.guild.get_member(int(user))).split('#')
                inv_len = len(inv)
                c = 0
                while c < inv_len:
                    item = str(inv[c]).split('~')
                    if item[0] == 'friend' and int(item[1]) > 0:
                        rand = 11
                    c = c + 1
                if rand <= 3:
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
                    logging_info(f'Response: {ctx.author.id} tried to kill {user}\n----------')
                elif rand == 11:
                    money = randint(0, (round(bala/2, 0)))
                    inv_len = len(inv)
                    c = 0
                    while c < inv_len:
                        item = str(inv[c]).split('~')
                        if item[0] == 'friend':
                            count = int(item[1]) - 1
                            inv[c] = f'friend~{count}'
                        c = c + 1
                    bala = bala - money
                    balb = balb + money
                    dab.collection('users').document(str(ctx.author.id)).update({'bal': bala})
                    dab.collection('users').document(str(user)).update({'bal': balb})
                    dab.collection('users').document(str(ctx.author.id)).update({'inv': inv})
                    await ctx.send(f'{a[0]} tried to kill {b[0]} with a gun, but their friend stopped them and handed them over to the police\n{b[0]} earned {money} coins and {a[0]} lost their gun')
                    logging_info(f'Response: {ctx.author.id} tried to kill {user}\n----------')
                else:
                    money = randint(0, (round(balb/2, 0)))
                    bala = bala + money
                    balb = balb - money
                    dab.collection('users').document(str(ctx.author.id)).update({'bal': bala})
                    dab.collection('users').document(str(user)).update({'bal': balb})
                    await ctx.send(f'{a[0]} killed {b[0]} using a gun\n{a[0]} found {money} coins in their wallet')
                    logging_info(f'Response: {ctx.author.id} killed {user}\n----------')
        else:
            await ctx.send('How are you going to use it if you don\'t even own it?')
            logging_info('Response: no gun in inv\n----------')

def setup(bot):
    bot.add_cog(items(bot))