import discord, os, requests, json, firebase_admin, asyncio
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

class User(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("User cog loaded")
    
    #User
    @commands.group(invoke_without_command=True)
    async def user(self, ctx, argument=None):
        if argument is not None:
            user = str(argument)
        else:
            user = str(f"<@!{ctx.author.id}>")
            ID = argument[3:]
            ID = ID[:-1]
            ctx.author = self.client.get_user(int(ID))
        print(f'Recieved: >user {user}')
        ref = dab.collection(user).document('data').get()
        username = ref.get('username')
        scoresaber = ref.get('scoresaber')
        birthday = ref.get('birthday')
        embed=discord.Embed(title=username, color=0xff0000)
        embed.add_field(name="Scoresaber", value=scoresaber, inline=False)
        embed.add_field(name="Birthday", value=birthday, inline=True)
        embed.set_footer(text="this code was ruined by ThiJNmEnS#6059")
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        print('Response: embed')
        print('----------')
        
    #User Add
    @user.command()
    async def add (self, ctx, argument=None, argument1=None, argument2=None, argument3=None):
        user = argument
        username = argument1
        scoresaber = argument2
        birthday = argument3
        print(f'Recieved: >user add {user}')
        print (user, username, scoresaber, birthday, ctx.author.id)
        authorid = str(f"<@!{ctx.author.id}>")
        print(authorid)
        if(user == authorid):
            #Get Username
            sent = await ctx.send('How would you like to be called?')
            try:
                msg = await self.client.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
                username = msg
                print(1)
                if msg:
                    sent = await ctx.send('What is your scoresaber link?')
                    try:
                        msg = await self.client.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
                        scoresaber = msg
                        print(2)
                        if msg:
                            sent = await ctx.send('When is your birthday? [DD/MM/YYYY]')
                            try:
                                msg = await self.client.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
                                birthday = msg
                                print(3)
                                print(username)
                                print(scoresaber)
                                print(birthday)
                                doc_ref = dab.collection(user).document('data')
                                doc_ref.set({
                                    'username':username,
                                    'scoresaber':scoresaber,
                                    'birthday':birthday})
                                await ctx.send(f'{username} has sucessfully been added to the database')
                                print(f'Response: {username} has sucessfully been added to the database')
                                print('----------')
                            except asyncio.TimeoutError:
                                await sent.delete()
                                await ctx.send('You did not reply in time, please restart the process')
                    except asyncio.TimeoutError:
                        await sent.delete()
                        await ctx.send('You did not reply in time, please restart the process')
            except asyncio.TimeoutError:
                await sent.delete()
                await ctx.send('You did not reply in time, please restart the process')
        else:
            await ctx.send('You can\'t add someone else to the database')
            print('You can\'t add someone else to the database')
            print('----------')
                
    #User Remove
    async def remove(self, ctx, argument1):
        user = argument1
        authorid = str(f"<@!{ctx.author.id}>")
        print(f'Recieved: >user remove {user}')
        if(user == authorid):
            dab.collection(user).document('data').delete()
            final = user + ' has sucessfully been removed to the database'
            await ctx.send(final)
            print(f'Response: {user} has sucessfully been removed to the database')
            print('----------')
        else:
            await ctx.send('You can\'t remove someone else to the database')
            print('You can\'t remove someone else to the database')
            print('----------')
                
    #User update
    async def update(self, ctx, argument1, argument2, argument3):
        user = argument1
        typec = argument2
        authorid = str(f"<@!{ctx.author.id}>")
        if(typec == 'username'):
            print(f'Recieved: >user update username {user}')
            username = argument3
            if(user == authorid):
                doc_ref = dab.collection(user).document('data')
                doc_ref.update({
                    'username':username})
                final = 'username has been updated'
                await ctx.send(final)
                print(f'Response: {user}\'s username has sucessfully been updated')
                print('----------')
        if(typec == 'scoresaber'):
            print(f'Recieved: >user update scoresaber {user}')
            scoresaber = argument3
            if(user == authorid):
                doc_ref = dab.collection(user).document('data')
                doc_ref.update({
                    'scoresaber':scoresaber})
                final = 'Scoresaber has been updated'
                await ctx.send(final)
                print(f'Response: {user}\'s scoresaber has sucessfully been updated')
                print('----------')
        if(typec == 'birthday'):
            print(f'Recieved: >user update birthday {user}')
            birthday = argument3
            if(user == authorid):
                doc_ref = dab.collection(user).document('data')
                doc_ref.update({
                    'birthday':birthday})
                final = 'birthday has been updated'
                await ctx.send(final)
                print(f'Response: {user}\'s birtday has sucessfully been updated')
                print('----------')
        if(typec != 'birtday' or 'scoresaber' or 'username'):
            await ctx.send('You can\'t update someone elses database')
            print('You can\'t update someone elses database')
            print('----------')

def setup(client):    
    client.add_cog(User(client))