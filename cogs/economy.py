import discord, logging
from discord.ext import commands
from firebase_admin import firestore

dab = firestore.client()

class economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=["s"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def shop(self, ctx):
        logging.info('Recieved shop') 
        embed = discord.Embed(
            title="Shop",
            description="Come and see, come and see! We have more then enough scams for you!",
            color=0xff0000)
        embed.add_field(name="<:PixelGun:806977728094928906> Gun", value='1000 Scuffed Coins\n ID: gun', inline=False)
        embed.add_field(name="<:adult:815178865475321868> Friend", value='2750 Scuffed Coins\n ID: friend', inline=False)
        await ctx.send(embed=embed)
        logging.info('Response: shop embed\n----------')
    
    @shop.command(case_insensitive=True, aliases=["gun"])
    async def shop_gun(self, ctx):
        logging.info('Recieved shop gun') 
        embed = discord.Embed(
            title="<:PixelGun:806977728094928906> Gun",
            description="Are we in texas or something?",
            color=0xff0000)
        embed.add_field(name="Buyable", value='Yes', inline=False)
        embed.add_field(name="Cost", value='1000 Scuffed Coins', inline=False)
        embed.add_field(name="Usable", value='Yes', inline=False)
        embed.add_field(name="Consumable", value='Yes', inline=False)
        await ctx.send(embed=embed)
        logging.info('Response: shop embed\n----------')
    
    @shop.command(case_insensitive=True, aliases=["friend"])
    async def shop_friend(self, ctx):
        logging.info('Recieved shop friend') 
        embed = discord.Embed(
            title="<:adult:815178865475321868> Friend",
            description="At least you can buy them...",
            color=0xff0000)
        embed.add_field(name="Buyable", value='Yes', inline=False)
        embed.add_field(name="Cost", value='2750 Scuffed Coins', inline=False)
        embed.add_field(name="Usable", value='no', inline=False)
        embed.add_field(name="Consumable", value='no', inline=False)
        await ctx.send(embed=embed)
        logging.info('Response: shop embed\n----------')
    
    @shop.group(invoke_without_command=True, case_insensitive=True)
    async def buy(self, ctx, argument=None):
        await ctx.send('Even i don\'t get what you are trying to buy master OwO?')
        logging.info('Response: Missing item to buy\n----------')

    @buy.command(case_insensitive=True, aliases=["gun"])
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
                    logging.info('Response: Gun has been bought\n----------')
                else:
                    await ctx.send(f'I didnt know you where poor master OwO, you need at least 1000 coins, you only have {bal}')
            a = a + 1
        
    @buy.command(case_insensitive=True, aliases=["friend"])
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
                    logging.info('Response: Friend has been bought\n----------')
                else:
                    await ctx.send(f'I didnt know you where poor master OwO, you need at least 2750 coins, you only have {bal}')
            a = a + 1
    
    @commands.command(case_insensitive=True, aliases=["inv"])
    async def inventory(self, ctx):
        logging.info('Recieved inv')
        embed = discord.Embed(
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
        embed.set_footer(text="this code was ruined by ThiJNmEnS and carried by Sirspam")
        await ctx.send(embed=embed)
        logging.info('Response: inv embed\n----------')
    
    @commands.command(case_insensitive=True)
    async def bal(self, ctx):
        logging.info('Recieved bal')
        bal = dab.collection('users').document(str(ctx.author.id)).get().get('bal')
        bank = dab.collection('users').document(str(ctx.author.id)).get().get('bank')
        await ctx.send(f'You have {bal} Scuffed Coins in your wallet and {bank} Coins in your bank')
        logging.info(f'Response: {ctx.author} has a bal of {bal} \n----------')

    @commands.command(case_insensitive=True, aliases=["dep"])
    async def deposit(self, ctx, argument):
        logging.info('Recieved deposit')
        bal = dab.collection('users').document(str(ctx.author.id)).get().get('bal')
        bank = dab.collection('users').document(str(ctx.author.id)).get().get('bank')
        if argument =='all':
            bank = bank + bal
            bal = 0
            dab.collection('users').document(str(ctx.author.id)).update({'bal': bal, 'bank': bank})
            await ctx.send(f'Wallet: {bal}\nBank: {bank}')
            logging.info(f'Response: {ctx.author} transferred all to bank \n----------')
        else:
            if int(argument) > bal:
                await ctx.send(f'You don\'t have enough money in your wallet to do that!')
                logging.info(f'Response: {ctx.author} did not have enough money\n----------')
            else:
                bank = bank + int(argument)
                bal = bal - int(argument)
                dab.collection('users').document(str(ctx.author.id)).update({'bal': bal, 'bank': bank})
                await ctx.send(f'Wallet: {bal}\nBank: {bank}')
                logging.info(f'Response: {ctx.author} transferred {argument} to bank \n----------')
    
    @commands.command(case_insensitive=True, aliases=["with"])
    async def withdraw(self, ctx, argument):
        logging.info('Recieved withdraw')
        bal = dab.collection('users').document(str(ctx.author.id)).get().get('bal')
        bank = dab.collection('users').document(str(ctx.author.id)).get().get('bank')
        if argument =='all':
            bal = bal + bank
            bank = 0
            dab.collection('users').document(str(ctx.author.id)).update({'bal': bal, 'bank': bank})
            await ctx.send(f'Wallet: {bal}\nBank: {bank}')
            logging.info(f'Response: {ctx.author} transferred all to bal \n----------')
        else:
            if int(argument) > bank:
                await ctx.send(f'You don\'t have enough money in your bank to do that!')
                logging.info(f'Response: {ctx.author} did not have enough money\n----------')
            else:
                bal = bal + int(argument)
                bank = bank - int(argument)
                dab.collection('users').document(str(ctx.author.id)).update({'bal': bal, 'bank': bank})
                await ctx.send(f'Wallet: {bal}\nBank: {bank}')
                logging.info(f'Response: {ctx.author} transferred {argument} to wallet \n----------')
    
    @commands.command(case_insensitive=True)
    @commands.has_permissions(administrator=True)
    async def gib(self, ctx, argument, argument2: int):
        logging.info('Recieved gib')
        if str(ctx.author.id) != '303017061637160961':
            if '@' in argument:
                argument = argument[3:]
                argument = argument[:-1]
            bal = dab.collection('users').document(argument).get().get('bal')
            bal = bal + int(argument2)
            dab.collection('users').document(argument).update({'bal': bal})
            a = ctx.guild.get_member(int(argument))
            await ctx.send(f'Given {argument2} Coins to {a.name}. their total is now {bal}')
            logging.info('Response: inv embed\n----------')
        else:
            await ctx.send(f'Fuck you james <:KEK:819309467208122388>')
            logging.info('Response: james is trying to cheat again...\n----------')

def setup(bot):
    bot.add_cog(economy(bot))