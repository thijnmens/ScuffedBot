#########################
#      Scuffed Bot      #
#########################
# Created by: Thijnmens #
#    Version: 1.1.0     #
#########################

import discord, os, logging
from discord.ext import commands
from discord.utils import get

intents = discord.Intents.default()
client = commands.Bot(command_prefix=">", intents=intents, case_insensitive=True)
client.remove_command('help')
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s: %(message)s',level=logging.INFO)
cwd = os.getcwd()
            
try: #literally copy and pasted this from one of my discord bots lol
    for filename in os.listdir(f'{cwd}/Cogs/'): #Heroku weird
        if filename.endswith(".py"):
           client.load_extension(f"Cogs.{filename[:-3]}")
except Exception as e:
    logging.critical(f"Possible fatal error:\n{e}\nThis means that the cogs have not started correctly!")

#Bot Startup
@client.event
async def on_ready():
    logging.info('Bot has successfully launched as {0.user}'.format(client))

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
            channel = message.channel
            user = command[2]
            print('Recieved: >user add ', user)
            userh = author.split('#')
            print(user)
            print(authorid)
            if(user == authorid):
                #add username
                await message.channel.send('How would you like to be called?')
                usernamesend = user
                def check(m):
                    return m.content == usernamesend and m.channel == channel
                
                msg = await client.wait_for('message', check=check)
                doc_ref = dab.collection(user).document('data')
                doc_ref.set({
                    'username':usernamesend,
                    'scoresaber':'NONE',
                    'birthday':'NONE'})
                #add scoresaber
                await message.channel.send('What is your scoresaber link?')
                scoresabersend = 'NONE'
                def check(m):
                    return m.content == scoresabersend and m.channel == channel
                
                msg = await client.wait_for('message', check=check)
                doc_ref = dab.collection(user).document('data')
                doc_ref.update({
                        'scoresaber':scoresabersend})
                #add birthday
                await message.channel.send('When is your birtday? [DD/MM/YYYY]')
                birthdaysend = 'NONE'
                def check(m):
                    return m.content == birthdaysend and m.channel == channel
                
                msg = await client.wait_for('message', check=check)
                doc_ref = dab.collection(user).document('data')
                doc_ref.update({
                        'birthday':birthdaysend})
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