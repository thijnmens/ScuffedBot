import discord, os, json, requests, schedule, time, firebase_admin, asyncio
from discord.ext import commands
from discord.utils import get
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db

cred = credentials.Certificate({
  "type": "service_account",
  "project_id": os.getenv("PROJECT_ID").replace('\\n', '\n'),
  "private_key_id": os.getenv("PRIVATE_KEY_ID").replace('\\n', '\n'),
  "private_key": os.getenv("PRIVATE_KEY").replace('\\n', '\n'),
  "client_email": os.getenv("CLIENT_EMAIL").replace('\\n', '\n'),
  "client_id": os.getenv("CLIENT_ID").replace('\\n', '\n'),
  "auth_uri": os.getenv("AUTH_URI").replace('\\n', '\n'),
  "token_uri": os.getenv("TOKEN_URI").replace('\\n', '\n'),
  "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL").replace('\\n', '\n'),
  "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL").replace('\\n', '\n')
})
default_app = firebase_admin.initialize_app(cred)
dab = firestore.client()

#Get Random Quote
def get_quote():
    responce = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(responce.text)
    quote = json_data[0]['q'] + ' -' + json_data[0]['a']
    return(quote)

#Check for birthdays
def get_birthdays():
    collectionlist = dab.collection_group()
    print(collectionlist)
    ref = dab.collection(collectionlist).document('data').get()
    username = ref.get('username')
    scoresaber = ref.get('scoresaber')
    birthday = ref.get('birthday')
schedule.every().day.at('12:00').do(get_birthdays)

while 1:
    schedule.run_pending()
    time.sleep(1)

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
        get_birthdays()
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
        embed.add_field(name=">user [mention]", value="get the info of a user", inline=False)
        embed.add_field(name=">user add", value="add yourself to the userbase, if you don't want to fill something in, pls use ``None``", inline=False)
        embed.add_field(name=">user update <mention> <field> <new value>", value="Update your info", inline=False)
        embed.add_field(name=">user remove <mention>", value="Removes your info from the database", inline=False)
        embed.add_field(name=">quote", value="idk, a random quote?", inline=False)
        embed.add_field(name=">hello", value="just... don't", inline=False)
        embed.set_footer(text="this code was ruined by ThiJNmEnS#6059")
        await ctx.send(embed=embed)
        print('Response: embed')
        print('----------')

def setup(client):    
    client.add_cog(Text(client))