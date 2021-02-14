import discord, logging, asyncio
from discord import client
from discord.ext import commands
from discord.utils import get
from firebase_admin import firestore

dab = firestore.client()

class items(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True, case_insensitive=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def use(self, ctx, argument=None):
        logging.info('Recieved: >use')
        await ctx.send('What do you want to use senpai?')
        logging.info('Response: missing arguments\n----------')
    
    @use.group(aliases=["gun"])
    async def use_gun(self, ctx):
        logging.info('Recieved: >use gun')
        try:
            sent = await ctx.send('Who do you want to use the gun on?')
            msg = await self.client.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
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
            a = str(ctx.guild.get_member(int(ctx.author.id))).split('#')
            b = str(ctx.guild.get_member(int(user))).split('#')
            await ctx.send(f'{a[0]} killed {b[0]} using a gun')
        logging.info(f'Response: {ctx.author.id} killed {user}\n----------')

def setup(client):
    client.add_cog(items(client))