from logging import info as logging_info
from random import randint
from datetime import datetime

from discord import Embed, DMChannel
from firebase_admin import firestore

from discord.ext import commands


dab = firestore.client()

class economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, aliases=["s"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def shop(self, ctx):
        embed = Embed(
            title="Shop",
            description="Come and see, come and see! We have more than enough scams for you!",
            color=0xff0000)
        embed.add_field(name="<:PixelGun:806977728094928906> Gun", value='1000 Scuffed Coins\n ID: gun', inline=False)
        embed.add_field(name="<:adult:815178865475321868> Friend", value='2750 Scuffed Coins\n ID: friend', inline=False)
        await ctx.send(embed=embed)
    
    @shop.command(aliases=["gun"])
    async def shop_gun(self, ctx):
        logging_info('Recieved >shop gun') 
        embed = Embed(
            title="<:PixelGun:806977728094928906> Gun",
            description="Are we in texas or something?",
            color=0xff0000)
        embed.add_field(name="Buyable", value='Yes', inline=False)
        embed.add_field(name="Cost", value='1000 Scuffed Coins', inline=False)
        embed.add_field(name="Usable", value='Yes', inline=False)
        embed.add_field(name="Consumable", value='Yes', inline=False)
        await ctx.send(embed=embed)
    
    @shop.command(aliases=["friend"])
    async def shop_friend(self, ctx):
        logging_info('Recieved >shop friend') 
        embed = Embed(
            title="<:adult:815178865475321868> Friend",
            description="At least you can buy them...",
            color=0xff0000)
        embed.add_field(name="Buyable", value='Yes', inline=False)
        embed.add_field(name="Cost", value='2750 Scuffed Coins', inline=False)
        embed.add_field(name="Usable", value='no', inline=False)
        embed.add_field(name="Consumable", value='no', inline=False)
        await ctx.send(embed=embed)
    
    @shop.group(invoke_without_command=True, )
    async def buy(self, ctx, argument=None):
        await ctx.send('Even i don\'t get what you are trying to buy master OwO?')
        logging_info('Response: Missing item to buy\n----------')

    @buy.command(aliases=["gun"])
    async def buy_gun(self, ctx):
        inv = dab.collection('users').document(str(ctx.author.id)).get().get('inv')
        bal = dab.collection('users').document(str(ctx.author.id)).get().get('bal')
        inv_len = len(inv)
        a = 0
        while a < inv_len:
            item = str(inv[a]).split('~')
            if item[0] == 'gun':
                if bal >= 1000:
                    count = int(item[1]) + 1
                    inv[a] = f'gun~{count}'
                    bal = bal - 1000
                    dab.collection('users').document(str(ctx.author.id)).update({'inv': inv, 'bal': bal})
                    await ctx.send(f'Gun has been added to your inv, you now own {count} guns')
                    logging_info('Response: Gun has been bought\n----------')
                else:
                    await ctx.send(f'I didnt know you where poor master OwO, you need at least 1000 coins, you only have {bal}')
            a = a + 1
        
    @buy.command(aliases=["friend"])
    async def buy_friend(self, ctx):
        inv = dab.collection('users').document(str(ctx.author.id)).get().get('inv')
        bal = dab.collection('users').document(str(ctx.author.id)).get().get('bal')
        inv_len = len(inv)
        a = 0
        while a < inv_len:
            item = str(inv[a]).split('~')
            if item[0] == 'friend':
                if bal >= 2750:
                    count = int(item[1]) + 1
                    inv[a] = f'friend~{count}'
                    bal = bal - 2750
                    dab.collection('users').document(str(ctx.author.id)).update({'inv': inv, 'bal': bal})
                    await ctx.send(f'Friend has been added to your inv, you now have {count} friends')
                    logging_info('Response: Friend has been bought\n----------')
                else:
                    await ctx.send(f'I didnt know you where poor master OwO, you need at least 2750 coins, you only have {bal}')
            a = a + 1
    
    @commands.command(aliases=["inv"])
    async def inventory(self, ctx):
        embed = Embed(
            title=f"Inventory of {ctx.author}",
            description="Look at all those great items!",
            color=0xff0000)
        inv = dab.collection('users').document(str(ctx.author.id)).get().get('inv')
        inv_len = len(inv)
        a = 0
        while a < inv_len:
            item = str(inv[a]).split('~')
            embed.add_field(name=item[0], value=item[1], inline=False)
            a = a + 1
        embed.set_footer(text="this code was ruined by ThiJNmEnS, carried by Sirspam and spelling mistakes corrected by notmyname")
        await ctx.send(embed=embed)
    
    @commands.command()
    async def bal(self, ctx):
        logging_info('Recieved >bal')
        bal = dab.collection('users').document(str(ctx.author.id)).get().get('bal')
        bank = dab.collection('users').document(str(ctx.author.id)).get().get('bank')
        await ctx.send(f'You have {bal} Scuffed Coins in your wallet and {bank} Coins in your bank')

    @commands.command(aliases=["dep"])
    async def deposit(self, ctx, argument):
        bal = dab.collection('users').document(str(ctx.author.id)).get().get('bal')
        bank = dab.collection('users').document(str(ctx.author.id)).get().get('bank')
        if argument =='all':
            bank = bank + bal
            bal = 0
            dab.collection('users').document(str(ctx.author.id)).update({'bal': bal, 'bank': bank})
            await ctx.send(f'Wallet: {bal}\nBank: {bank}')
        else:
            if int(argument) > bal:
                await ctx.send(f'You don\'t have enough money in your wallet to do that!')
                logging_info(f'Response: {ctx.author} did not have enough money\n----------')
            else:
                bank = bank + int(argument)
                bal = bal - int(argument)
                dab.collection('users').document(str(ctx.author.id)).update({'bal': bal, 'bank': bank})
                await ctx.send(f'Wallet: {bal}\nBank: {bank}')
    
    @commands.command(aliases=["with"])
    async def withdraw(self, ctx, argument):
        bal = dab.collection('users').document(str(ctx.author.id)).get().get('bal')
        bank = dab.collection('users').document(str(ctx.author.id)).get().get('bank')
        if argument =='all':
            bal = bal + bank
            bank = 0
            dab.collection('users').document(str(ctx.author.id)).update({'bal': bal, 'bank': bank})
            await ctx.send(f'Wallet: {bal}\nBank: {bank}')
            logging_info(f'Response: {ctx.author} transferred all to bal \n----------')
        else:
            if int(argument) > bank:
                await ctx.send(f'You don\'t have enough money in your bank to do that!')
                logging_info(f'Response: {ctx.author} did not have enough money\n----------')
            else:
                bal = bal + int(argument)
                bank = bank - int(argument)
                dab.collection('users').document(str(ctx.author.id)).update({'bal': bal, 'bank': bank})
                await ctx.send(f'Wallet: {bal}\nBank: {bank}')
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def gib(self, ctx, argument, argument2: int):
        if str(ctx.author.id) != '303017061637160961':
            if '@' in argument:
                argument = argument[3:]
                argument = argument[:-1]
            bal = dab.collection('users').document(argument).get().get('bal')
            bal = bal + int(argument2)
            dab.collection('users').document(argument).update({'bal': bal})
            a = ctx.guild.get_member(int(argument))
            await ctx.send(f'Given {argument2} Coins to {a.name}. their total is now {bal}')
            logging_info('Response: inv embed\n----------')
        else:
            await ctx.send(f'Fuck you james <:KEK:819309467208122388>')
            logging_info('Response: james is trying to cheat again...\n----------')
    
    @commands.command()
    @commands.cooldown(1, 43200, commands.BucketType.user)
    async def heist(self, ctx, argument):
        HeistMembers = []
        if (argument.startswith('<@') == True and argument.endswith('>') == True):
            victimID = int(str(argument.split('!')[1]).split('>')[0])
            await ctx.send(f'Good luck robbing {str(ctx.guild.get_member(victimID))} Senpai! Others can do `join` to join the heist btw :)\nType `start` to start the heist!')
            HeistMembers.append(ctx.author.id)
            while True:
                msg = await self.bot.wait_for('message', check=lambda message: message.channel == ctx.channel)
                if msg.content.lower() == 'start':
                    finish = randint(1,5)
                    await ctx.send(f'Starting the heist on {str(ctx.guild.get_member(victimID))} with {len(HeistMembers)} people, good luck! UwU\nEstimated time till finish: {finish} Minutes')
                    endloop = datetime.datetime.now() + datetime.timedelta(minutes=finish)
                    victimMsg = ''
                    user = await self.bot.fetch_user(victimID)
                    await DMChannel.send(user, f'{ctx.author} Is trying to rob your bank! Go to the Scuffed Tourneys server and quickly stop them by typing either `police` or `stop` in the channel where the heist was started!')
                    while True:
                        try:
                            victimMsg = await self.bot.wait_for('message', timeout=1, check=lambda message: message.author.id == victimID and message.channel == ctx.channel)
                            if victimMsg.content.lower() == 'police' or victimMsg.content.lower() == 'stop':
                                for HeistMemberID in HeistMembers:
                                    inv = dab.collection('users').document(str(HeistMemberID)).get().get('inv')
                                    newinv = []
                                    for item in inv:
                                        newinv.append(str(item.split('~')[0]) + '~0')
                                    dab.collection('users').document(str(HeistMemberID)).update({'inv': newinv})
                                await ctx.send(f'The heist was a utter failure! Your team got sent to prison and they lost every item in their inventory, better luck next time!')
                                break
                        except Exception:
                            if datetime.datetime.now() > endloop:
                                if len(HeistMembers) <= 3:
                                    chance = randint(0, 100)
                                elif len(HeistMembers) <= 5:
                                    chance = randint(0, 75)
                                elif len(HeistMembers) <= 7:
                                    chance = randint(0, 50)
                                elif len(HeistMembers) > 7:
                                    chance = randint(0, 25)
                                if chance <= 20:
                                    #Sucess
                                    bal = dab.collection('users').document(str(victimID)).get().get('bank')
                                    stolen = randint(bal / 2, bal)
                                    newbank = bal - stolen
                                    dab.collection('users').document(str(victimID)).update({'bank': newbank})
                                    stolenPerMember = int(stolen / len(HeistMembers))
                                    for HeistMemberID in HeistMembers:
                                        bal = dab.collection('users').document(str(HeistMemberID)).get().get('bal')
                                        newbal = bal + stolenPerMember
                                        dab.collection('users').document(str(HeistMemberID)).update({'bal': newbal})
                                    await ctx.send(f'The heist was sucessfull! Your team stole {stolen} coins and this was evenly distributed among {len(HeistMembers)} crewmembers ({stolenPerMember} Coins Each)')
                                else:
                                    #Failure
                                    for HeistMemberID in HeistMembers:
                                        inv = dab.collection('users').document(str(HeistMemberID)).get().get('inv')
                                        newinv = []
                                        for item in inv:
                                            newinv.append(str(item.split('~')[0]) + '~0')
                                        dab.collection('users').document(str(HeistMemberID)).update({'inv': newinv})
                                    await ctx.send(f'The heist was a utter failure! Your team got sent to prison and they lost every item in their inventory, better luck next time!')
                                break
                            else:
                                continue
                        break
                    break
                elif msg.content.lower() == 'stop':
                    await ctx.send('Stopped the heist')
                    #heist.reset_cooldown(ctx)
                    break
                elif msg.content.lower() == 'list':
                    memberstring = 'Members:\n'
                    for member in HeistMembers:
                        memberstring = memberstring + str(ctx.guild.get_member(member)).split('#')[0] + '\n'
                    await ctx.send(memberstring)   
                elif msg.content.lower() == 'join':
                    exists = msg.author.id in HeistMembers
                    if (exists == True):
                        await ctx.send(f'You are already part of this heist Senpai')   
                    else:
                        HeistMembers.append(msg.author.id)
        elif (argument.lower() == 'help'):
            await ctx.send('*<Insert help embed here>*')
            #commands.command.reset_cooldown(ctx)
        else:
            logging_info("MissingRequiredArgument handler ran\n----------")
            await ctx.send(f"You didn't give a required argument, B-Baka!")
            #commands.reset_cooldown(ctx)
        print('----------')
            
def setup(bot):
    bot.add_cog(economy(bot))