#########################
#      Scuffed Bot      #
#########################
# Created by: Thijnmens #
#    Version: 1.0.0     #
#########################

import discord
import os
import requests
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db

client = discord.Client()
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

#Bot Startup
@client.event
async def on_ready():
    print('Bot has successfully launched as {0.user}'.format(client))

#Get Random Quote
def get_quote():
    responce = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(responce.text)
    quote = json_data[0]['q'] + ' -' + json_data[0]['a']
    return(quote)


#Commands List
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content
    author = str(message.author)
    a = str(message.author.id)
    authorid = '<@!' + a + '>'

    #test
    if message.content.startswith('>test'):
        print('Recieved: >test')
        print(author)
        print(msg)
        print(message.author.id)
        print(authorid)
        await message.channel.send('testing complete')
        print('Response: testing complete')
        print('----------')

    
    #Hello
    if message.content.startswith('>hello'):
        print('Recieved: >hello')
        await message.channel.send('Owo')
        print('Response: Owo')
        print('----------')

    #Quote
    if message.content.startswith('>quote'):
        print('Recieved: >quote')
        final = get_quote()
        await message.channel.send(final)
        print('Response: ', final)
        print('----------')
    
    #Help
    if message.content.startswith('>help'):
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
        await message.channel.send(embed=embed)
        print('Response: embed')
        print('----------')

    #User
    if message.content.startswith('>user'):
        command = ['None', 'None', 'None', 'None', 'None', 'None']
        command = msg.split(' ')
        
        #User Add
        if(command[1] == 'add'):
            user = command[2]
            username = command[3]
            scoresaber = command[4]
            birthday = command [5]
            print('Recieved: >user add ', user)
            userh = author.split('#')
            print(user)
            print(authorid)
            if(user == authorid):
                doc_ref = dab.collection(user).document('data')
                doc_ref.set({
                    'username':username,
                    'scoresaber':scoresaber,
                    'birthday':birthday})
                final = user + ' has sucessfully been added to the database'
                await message.channel.send(final)
                print('Response: ', user, ' has sucessfully been added to the database')
                print('----------')
            else:
                await message.channel.send('You can\'t add someone else to the database')
                print('You can\'t add someone else to the database')
                print('----------')
                
        #User Remove
        if(command[1] == 'remove'):
            user = command[2]
            print('Recieved: >user remove ', user)
            if(user == authorid):
                dab.collection(user).document('data').delete()
                final = user + ' has sucessfully been removed to the database'
                await message.channel.send(final)
                print('Response: ', user, ' has sucessfully been removed to the database')
                print('----------')
            else:
                await message.channel.send('You can\'t remove someone else to the database')
                print('You can\'t remove someone else to the database')
                print('----------')
                
        #User update
        if(command[1] == 'update'):
            user = command[2]
            typec = command[3]
            if(typec == 'username'):
                print('Recieved: >user update username', user)
                username = command[4]
                userh = author.split('#')
                if(user == authorid):
                    doc_ref = dab.collection(user).document('data')
                    doc_ref.update({
                        'username':username})
                    final = 'username has been updated'
                    await message.channel.send(final)
                    print('Response: ', user, '\'s username has sucessfully been updated')
                    print('----------')
            if(typec == 'scoresaber'):
                print('Recieved: >user update scoresaber', user)
                scoresaber = command[4]
                userh = author.split('#')
                if(user == authorid):
                    doc_ref = dab.collection(user).document('data')
                    doc_ref.update({
                        'scoresaber':scoresaber})
                    final = 'Scoresaber has been updated'
                    await message.channel.send(final)
                    print('Response: ', user, '\'s scoresaber has sucessfully been updated')
                    print('----------')
            if(typec == 'birthday'):
                print('Recieved: >user update birthday', user)
                birthday = command[4]
                userh = author.split('#')
                if(user == authorid):
                    doc_ref = dab.collection(user).document('data')
                    doc_ref.update({
                        'birthday':birthday})
                    final = 'birthday has been updated'
                    await message.channel.send(final)
                    print('Response: ', user, '\'s birtday has sucessfully been updated')
                    print('----------')
            if(typec != 'birtday' or 'scoresaber' or 'username'):
                await message.channel.send('You can\'t update someone elses database')
                print('You can\'t update someone elses database')
                print('----------')
        else:
            user = str(command[1])
            print('Recieved: >user ', user)
            ref = dab.collection(user).document('data').get()
            username = ref.get('username')
            scoresaber = ref.get('scoresaber')
            birthday = ref.get('birthday')
            embed=discord.Embed(title=username, color=0xff0000)
            embed.add_field(name="Scoresaber", value=scoresaber, inline=False)
            embed.add_field(name="Birthday", value=birthday, inline=True)
            embed.set_footer(text="this code was ruined by ThiJNmEnS#6059")
            await message.channel.send(embed=embed)
            print('Response: embed')
            print('----------')
            
#Login to discord   
client.run(os.getenv("TOKEN"))
