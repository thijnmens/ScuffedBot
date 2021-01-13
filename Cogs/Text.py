import discord, os, json, requests
from discord.ext import commands, tasks
from discord.utils import get

#Get Random Quote
def get_quote():
    response = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(response.text)
    quote = (f"{json_data[0]['q']} - {json_data[0]['a']}")
    return(quote)

class Text(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Text cog loaded")

    #Commands List
    @commands.Cog.listener('on_message')
    async def on_message(self, message):
        if message.author == self.client.user:
            return
    
    #ping
    @commands.command()
    async def ping(self, ctx):
        print('Recieved: >ping')
        await ctx.send(f'uwu *notices your ping* <w< ``{round(self.client.latency * 1000)}ms``')
        print(f'Response: {round(self.client.latency * 1000)}')
        print('----------')

    @commands.command(aliases=["no"]) #Keep this out of the help embed ;)
    @commands.cooldown(1, 120, commands.BucketType.guild)
    async def nope(self, ctx):
        print("Recieved >nope")
        await ctx.send("Join the NOPE clan <:GunChamp:796047943966523432>\nhttps://discord.gg/xH7AGnGXkf")
        print ("Response: Certainly not a link to the NOPE discord")
        print('----------')
    
    #Quote
    @commands.command()
    async def quote(self, ctx):
        print('Recieved: >quote')
        final = get_quote()
        await ctx.send(final)
        print(f'Response: {final}')
        print('----------')

def setup(client):    
    client.add_cog(Text(client))