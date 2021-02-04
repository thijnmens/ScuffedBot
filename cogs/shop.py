import discord
import logging
from discord.ext import commands
from discord.utils import get
from firebase_admin import firestore

dab = firestore.client()

class shop(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True, case_insensitive=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def shop(self, ctx, argument=None, argument2=None):
        logging.info('Recieved: >shop') 
        if(argument==None):
            embed = discord.Embed(
                title="Shop",
                description="Come and see, come and see! We have more then enough scams for you!",
                color=0xff0000)
            embed.add_field(name="<:PixelGun:806984027520761856> Gun", value='1000 Scuffed Coins\n ID: gun', inline=False)
            embed.set_footer(text="this code was ruined by ThiJNmEnS and carried by Sirspam")
            await ctx.send(embed=embed)
            logging.info('Response: shop embed\n----------')
        elif(argument.lower()=='buy'):
            if(argument2.lower()==gun):
                ctx.send('Your mom')
        elif(argument.lower()=='gun'):
            embed = discord.Embed(
                title="<:PixelGun:806984027520761856> Gun",
                description="Are we in texas or something?",
                color=0xff0000)
            embed.add_field(name="Buyable", value='Yes', inline=False)
            embed.add_field(name="Cost", value='1000 Scuffed Coins', inline=False)
            embed.add_field(name="Usable", value='Yes', inline=False)
            embed.add_field(name="Consumable", value='Yes', inline=False)
            embed.set_footer(text="this code was ruined by ThiJNmEnS and carried by Sirspam")
            await ctx.send(embed=embed)
            logging.info('Response: shop embed\n----------')



def setup(client):
    client.add_cog(shop(client))