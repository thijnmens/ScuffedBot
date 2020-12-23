import discord, os, requests, json, firebase_admin, logging
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
    
    #User
    @commands.group(invoke_without_command=True)
    async def user(self, ctx, argument=None):
        if argument is not None:
            user = str(argument)
        else:
            user = ctx.author.name
        user = str(argument)
        logging.info(f'Recieved: >user {user}')
        ref = dab.collection(user).document('data').get()
        username = ref.get('username')
        scoresaber = ref.get('scoresaber')
        birthday = ref.get('birthday')
        embed=discord.Embed(title=username, color=0xff0000)
        embed.add_field(name="Scoresaber", value=scoresaber, inline=False)
        embed.add_field(name="Birthday", value=birthday, inline=True)
        embed.set_footer(text="this code was ruined by ThiJNmEnS#6059")
        await ctx.send(embed=embed)
        logging.info('Response: embed')
        logging.info('----------')
        
    #User Add
    @user.command()
    async def add (self, ctx, argument1, argument2, argument3, argument4):
        user = argument1
        username = argument2
        scoresaber = argument3
        birthday = argument4
        logging.info(f'Recieved: >user add {user}')
        authorid = ("!<@"+ctx.author.id+">")
        print(authorid)
        if(user == authorid):
            doc_ref = dab.collection(user).document('data')
            doc_ref.set({
                'username':username,
                'scoresaber':scoresaber,
                'birthday':birthday})
            final = f'{user} has sucessfully been added to the database'
            await ctx.send(final)
            logging.info(f'Response: {user} has sucessfully been added to the database')
            logging.info('----------')
        else:
            await ctx.send('You can\'t add someone else to the database')
            logging.info('You can\'t add someone else to the database')
            logging.info('----------')
                
    #User Remove
    async def remove(self, ctx, argument1):
        user = argument1
        authorid = ("!<@"+ctx.author.id+">")
        logging.info(f'Recieved: >user remove {user}')
        if(user == authorid):
            dab.collection(user).document('data').delete()
            final = user + ' has sucessfully been removed to the database'
            await ctx.send(final)
            logging.info(f'Response: {user} has sucessfully been removed to the database')
            logging.info('----------')
        else:
            await ctx.send('You can\'t remove someone else to the database')
            logging.info('You can\'t remove someone else to the database')
            logging.info('----------')
                
    #User update
    async def update(self, ctx, argument1, argument2, argument3):
        user = argument1
        typec = argument2
        authorid = ("!<@"+ctx.author.id+">")
        if(typec == 'username'):
            logging.info(f'Recieved: >user update username {user}')
            username = argument3
            if(user == authorid):
                doc_ref = dab.collection(user).document('data')
                doc_ref.update({
                    'username':username})
                final = 'username has been updated'
                await ctx.send(final)
                logging.info(f'Response: {user}\'s username has sucessfully been updated')
                logging.info('----------')
        if(typec == 'scoresaber'):
            logging.info(f'Recieved: >user update scoresaber {user}')
            scoresaber = argument3
            if(user == authorid):
                doc_ref = dab.collection(user).document('data')
                doc_ref.update({
                    'scoresaber':scoresaber})
                final = 'Scoresaber has been updated'
                await ctx.send(final)
                logging.info(f'Response: {user}\'s scoresaber has sucessfully been updated')
                logging.info('----------')
        if(typec == 'birthday'):
            logging.info(f'Recieved: >user update birthday {user}')
            birthday = argument3
            if(user == authorid):
                doc_ref = dab.collection(user).document('data')
                doc_ref.update({
                    'birthday':birthday})
                final = 'birthday has been updated'
                await ctx.send(final)
                logging.info(f'Response: {user}\'s birtday has sucessfully been updated')
                logging.info('----------')
        if(typec != 'birtday' or 'scoresaber' or 'username'):
            await ctx.send('You can\'t update someone elses database')
            logging.info('You can\'t update someone elses database')
            logging.info('----------')

def setup(client):    
    client.add_cog(User(client))