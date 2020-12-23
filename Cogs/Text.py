import discord, os, json, requests
from discord.ext import commands
from discord.utils import get

#Get Random Quote
def get_quote():
    responce = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(responce.text)
    quote = json_data[0]['q'] + ' -' + json_data[0]['a']
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

    #Test
    @commands.command()
    async def test(self, ctx):
        print('Recieved: >test')
        print(ctx.message.author)
        print(ctx.message.content)
        print(ctx.message.author.id)
        await ctx.send('testing complete')
        print('Response: testing complete')
        print('----------')

    #Hello
    @commands.command()
    async def hello(self, ctx):
        print('Recieved: >hello')
        await ctx.send('Owo')
        print('Response: Owo')
        print('----------')

    #Quote
    @commands.command()
    async def quote(self, ctx):
        print('Recieved: >quote')
        final = get_quote()
        await ctx.send(final)
        print(f'Response: {final}')
        print('----------')
    
    #Help
    @commands.command()
    async def help(self, ctx):
        print('Recieved: >help ')
        embed=discord.Embed(title="Help", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", description="You can find all kinds of commands here, most of them are probably broken", color=0xff0000)
        embed.set_author(name="Thijnmens", url="https://github.com/thijnmens/", icon_url="https://cdn.discordapp.com/avatars/490534335884165121/eaeff60636ebf53040d8d5c0761c6c67.png?size=256")
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/790189114711605260/c6e486bab141b997eeceb42ac5c9a3c2.png?size=256")
        embed.add_field(name=">help", value="this fancy page", inline=False)
        embed.add_field(name=">user <mention>", value="get the info of a user", inline=False)
        embed.add_field(name=">user add <mention> <username> <scoresaber> <b-day>", value="add yourself to the userbase, if you don't want to fill something in, pls use NONE", inline=False)
        embed.add_field(name=">user update <mention> <field> <new value>", value="Update your info", inline=False)
        embed.add_field(name=">quote", value="idk, a random quote?", inline=False)
        embed.add_field(name=">hello", value="just... don't", inline=False)
        embed.set_footer(text="this code was ruined by ThiJNmEnS#6059")
        await ctx.send(embed=embed)
        print('Response: embed')
        print('----------')

def setup(client):    
    client.add_cog(Text(client))