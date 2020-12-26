import discord, os, json, requests
from discord.ext import commands
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

    #Hello
    @commands.command()
    async def ping(self, ctx):
        print('Recieved: >ping')
        await ctx.send(f'uwu *notices your ping* Owo ``{round(self.client.latency * 1000)}ms``')
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
        embed=discord.Embed(title="Help", url="https://www.youtube.com/watch?v=7LnQRFh_knk", description="You can find all kinds of commands here, most of them are probably broken", color=0xff0000)
        embed.set_author(name="Thijnmens", url="https://github.com/thijnmens/", icon_url="https://cdn.discordapp.com/avatars/490534335884165121/eaeff60636ebf53040d8d5c0761c6c67.png?size=256")
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/790189114711605260/c6e486bab141b997eeceb42ac5c9a3c2.png?size=256")
        embed.add_field(name=">help", value="this fancy page", inline=False)
        embed.add_field(name=">user [mention]", value="get the info of a user", inline=False)
        embed.add_field(name=">user add", value="add yourself to the userbase, if you don't want to fill something in, pls use ``None``", inline=False)
        embed.add_field(name=">user update <field> <new value>", value="Update your info", inline=False)
        embed.add_field(name=">user remove", value="Removes your info from the database", inline=False)
        embed.add_field(name=">scoresaber [mention]", value="gets a user's ScoreSaber data,",inline=False)
        embed.add_field(name=">scoresaber topsong [mention]", value="gets a user's top song from ScoreSaber,",inline=False)
        embed.add_field(name=">scoresaber recentsong [mention]", value="gets a user's most recent song from ScoreSaber,",inline=False)
        embed.add_field(name=">quote", value="Posts a random quote", inline=False)
        embed.add_field(name=">ping", value="Pings Scuffed Bot", inline=False)
        embed.set_footer(text="this code was ruined by ThiJNmEnS#6059")
        await ctx.send(embed=embed)
        print('Response: help embed')
        print('----------')

def setup(client):    
    client.add_cog(Text(client))