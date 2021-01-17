import discord, os, requests, json, firebase_admin, asyncio, time, re
from discord.ext import commands
from discord.utils import get
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db

dab = firestore.client()

class User(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.valid_HMD = ["CV1","Rift S","Quest","Quest 2","Index","Vive","WMR"]

    @commands.Cog.listener()
    async def on_ready(self):
        print("User cog loaded")

    #User
    @commands.group(invoke_without_command=True, case_insensitive=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def user(self, ctx, argument=None):
        if argument is not None:
            if argument.isdigit():
                ctx.author = self.client.get_user(int(argument))
                if ctx.author is None:
                    return await ctx.send("Sorry Senpai, I can't find anyone with that ID qwq")

            else:
                ID = argument[3:]
                ID = ID[:-1]
                ctx.author = self.client.get_user(int(ID))
        print(f'Recieved: >user {ctx.author.name}')
        ref = dab.collection(str(ctx.author.id)).document('data').get()
        username = ref.get("username")
        if username is None:
            print (f"User not found")
            if argument is None:
                return await ctx.send("You're not in my database, Senpai! qwq\nYou should use ``>user add`` <w<")
            elif argument is not None:
                return await ctx.send("That person isn't in my database qwq")
        scoresaber = ref.get("scoresaber")
        try:
            steam = ref.get("steam")
        except:
            steam = None
        try:
            twitch = ref.get("twitch")
        except:
            twitch = None
        try:
            youtube = ref.get("youtube")
        except:
            youtube = None
        try:
            twitter = ref.get("twitter")
        except:
            twitter = None
        try:
            reddit = ref.get("reddit")
        except:
            reddit = None
        try:
            hmd = ref.get("hmd")
        except:
            hmd = None
        try:
            birthday = ref.get("birthday")
        except:
            birthday = None
        try:
            pfp = ref.get("pfp")
        except:
            pfp = None
        try:
            status = ref.get("status")
        except:
            status = None
        #try: 
        #   this on for size, Mister
        links_Message = f"[Scoresaber]({scoresaber}) "
        if steam is not None:
            links_Message = links_Message+f"| [Steam]({steam}) "
        if twitch is not None:
            links_Message = links_Message+f"| [Twitch]({twitch}) "
        if youtube is not None:
            links_Message = links_Message+f"| [Youtube]({youtube})"
        if twitter is not None:
            links_Message = links_Message+f"| [Twitter]({twitter})"
        if reddit is not None:
            links_Message = links_Message+f"| [Reddit]({reddit})"
        try:
            colourRaw = ref.get("colour")
            colour = await commands.ColourConverter().convert(ctx, colourRaw)
            embed=discord.Embed(title=username, colour=colour)
        except Exception as e:
            embed=discord.Embed(title=username, colour=discord.Colour.random())
            print (f"Funny colour exception: {e}")
        embed.add_field(name="Links", value=links_Message, inline=False)
        if hmd is not None:
            embed.add_field(name="HMD", value=hmd, inline=True)
        if birthday is not None:
            embed.add_field(name="Birthday", value=birthday, inline=True)
        if status is not None:
            embed.add_field(name="Status", value=status, inline=False)
        if pfp is not None:
            embed.set_thumbnail(url=pfp)
        else:
            embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)
        print('Response: user embed')
        print('----------')
        
    #User Add
    @user.command()
    async def add (self, ctx, argument=None):
        print(f'Recieved: >user add {ctx.author.name}')
        sent = await ctx.send('What is your scoresaber link?')
        if argument is None:
            try:
                msg = await self.client.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
                scoresaber = msg.content
                scoresaber = scoresaber.split("?", 1)[0]
                scoresaber = scoresaber.split("&", 1)[0]
                doc_ref = dab.collection(str(ctx.author.id)).document('data')
                doc_ref.set({
                    'a':False,
                    'username':ctx.author.name,
                    'scoresaber':scoresaber,})
                try:
                    col_ref = dab.collection('collectionlist').document('data').get().get('collectionarray')
                    col_ref.append(str(ctx.author.id))
                    dab.collection('collectionlist').document('data').update({
                        'collectionarray':col_ref})
                except Exception as e:
                    print(e)
            except asyncio.TimeoutError:
                await sent.delete()
                await ctx.send('You did not reply in time, please restart the process')
                print ("Timed out")
                return print ("----------")
        else: #haha lazy copy and paste
            scoresaber = argument
            scoresaber = scoresaber.split("?", 1)[0]
            scoresaber = scoresaber.split("&", 1)[0]
            doc_ref = dab.collection(str(ctx.author.id)).document('data')
            doc_ref.set({
                'a':False,
                'username':ctx.author.name,
                'scoresaber':scoresaber,})
            try:
                col_ref = dab.collection('collectionlist').document('data').get().get('collectionarray')
                col_ref.append(str(ctx.author.id))
                dab.collection('collectionlist').document('data').update({
                    'collectionarray':col_ref})
            except Exception as e:
                print(e)
        await ctx.send(f'{ctx.author.name} has sucessfully been added to the database!\nUse ``>user update`` to add optional customisation')
        print(f'Response: {ctx.author.name} has sucessfully been added to the database')
        print('----------')
                
    #User Remove
    @user.command()
    async def remove(self, ctx):
        try:
            col_ref = dab.collection('collectionlist').document('data').get().get('collectionarray')
            col_ref.remove(str(ctx.author.id))
            dab.collection('collectionlist').document('data').get
            await ctx.send(f"{ctx.author.name} has been successfully removed from the database")
            print(f"Response: {ctx.author.id} has been successfully removed to the database")
            print('----------')
        except Exception as e:
            print(e)
                
    #User update
    @user.group(invoke_without_command=True, case_insensitive=True)
    async def update(self, ctx):
        print(f"Recieved: >user update")
        await ctx.send("B-Baka!! You need to tell me what you want to update!!\nUse ``>help update`` to check the valid arguments")
        print("no sub command given")
        print("---------")
        
    @update.command()
    async def username(self, ctx, *, argument):
        print(f'Recieved: >user update username {ctx.author.name}')
        doc_ref = dab.collection(str(ctx.author.id)).document('data')
        doc_ref.update({
            'username':argument})
        await ctx.send(f"I've updated Senpai's username to {argument}! >w<")
        print(f"{ctx.author.name} has updated their username to {argument}")
        print('----------')
    
    @update.command()
    async def scoresaber(self, ctx, argument):
        print(f'Recieved: >user update scoresaber {ctx.author.name}')
        argument = argument.split("?", 1)[0]
        argument = argument.split("&", 1)[0]
        doc_ref = dab.collection(str(ctx.author.id)).document('data')
        doc_ref.update({
            'scoresaber':argument})
        await ctx.send("I've updated your Scoresaber, Senpai! >w<")
        print(f"{ctx.author.name} has updated their scoresaber to {argument}")
        print('----------')

    @update.command()
    async def steam(self, ctx, argument):
        print(f'Recieved: >user update steam {ctx.author.name}')
        doc_ref = dab.collection(str(ctx.author.id)).document('data')
        doc_ref.update({
            'steam':argument})
        await ctx.send("I've updated your Steam, Senpai! >w<")
        print(f"{ctx.author.name} has updated their steam to {argument}")
        print('----------')
    
    @update.command()
    async def twitch(self, ctx, argument):
        print(f'Recieved: >user update twitch {ctx.author.name}')
        doc_ref = dab.collection(str(ctx.author.id)).document('data')
        doc_ref.update({
            'twitch':argument})
        await ctx.send("I've updated your Twitch, Senpai! >w<")
        print(f"{ctx.author.name} has updated their twitch to {argument}")
        print('----------')

    @update.command()
    async def youtube(self, ctx, argument):
        print(f'Recieved: >user update youtube {ctx.author.name}')
        doc_ref = dab.collection(str(ctx.author.id)).document('data')
        doc_ref.update({
            'youtube':argument})
        await ctx.send("I've updated your Youtube, Senpai! >w<")
        print(f"{ctx.author.name} has updated their youtube to {argument}")
        print('----------')
    
    @update.command()
    async def twitter(self, ctx, argument):
        print(f'Recieved: >user update twitter {ctx.author.name}')
        doc_ref = dab.collection(str(ctx.author.id)).document('data')
        doc_ref.update({
            'twitter':argument})
        await ctx.send("I've updated your Twitter, Senpai! >w<")
        print(f"{ctx.author.name} has updated their twitter to {argument}")
        print('----------')

    @update.command()
    async def reddit(self, ctx, argument):
        print(f'Recieved: >user update reddit {ctx.author.name}')
        doc_ref = dab.collection(str(ctx.author.id)).document('data')
        doc_ref.update({
            'reddit':argument})
        await ctx.send("I've updated your Reddit, Senpai! >w<")
        print(f"{ctx.author.name} has updated their reddit to {argument}")
        print('----------')

    @update.command()
    async def birthday(self, ctx, argument):
        print(f'Recieved: >user update birthday {ctx.author.name}')
        if ((bool(re.search(r"\d/", argument)))) is False:
            print ("Birthday input validation triggered")
            await ctx.send("Oopsie, looks like you did a woopsie! uwu\n``Don't use characters expect for numbers and /``")
            return
        storer = argument.split('/')
        storer[0] = int(storer[0])
        storer[1] = int(storer[1])
        if(storer[1]>12 or storer[1]<1 or storer[0]>31 or storer[0]<1):
            print ("Birthday legitimacy triggered")
            return await ctx.send("B-Baka!! that date doesn't make any sense!\n``Please use a legitimate date``")
        doc_ref = dab.collection(str(ctx.author.id)).document('data')
        doc_ref.update({
            'birthday':argument})
        await ctx.send(f"I've updated Senpai's birthday to {argument}! >w<")
        print(f"{ctx.author.name} has updated their birthday to {argument}")
        print('----------')
    
    @update.command()
    async def hmd(self, ctx, *, argument):
        print(f'Recieved: >user update hmd {ctx.author.name}')
        valid_HMD_low = [x.lower() for x in self.client.valid_HMD]
        if argument.lower() not in valid_HMD_low:
            print (f"{argument} not in valid_HMD")
            return await ctx.send("BAKA!! That HMD isn't valid!\n``Use >help update to check the valid HMDs``")
        doc_ref = dab.collection(str(ctx.author.id)).document('data')
        doc_ref.update({
            'hmd':argument})
        await ctx.send(f"I've updated Senpai's HMD to {argument}! >w<")
        print(f"{ctx.author.name} has updated their status to {argument}")
        print('----------')
    
    @update.command()
    async def pfp(self, ctx, argument):
        print (f"Recieved: >user update pfp {ctx.author.name}")
        doc_ref = dab.collection(str(ctx.author.id)).document('data')
        doc_ref.update({
            'pfp':argument})
        await ctx.send("I've updated your pfp, Senpai! >w<")
        print(f"{ctx.author.name} has updated their pfp to {argument}")
        print('----------')
    
    @update.command()
    async def status(self, ctx, *, argument):
        print(f'Recieved: >user update status {ctx.author.name}')
        doc_ref = dab.collection(str(ctx.author.id)).document('data')
        doc_ref.update({
            'status':argument})
        await ctx.send("I've updated your status, Senpai! >w<")
        print(f"{ctx.author.name} has updated their status to {argument}")
        print('----------')
    
    @update.command(aliases=["color"]) #Americans ew
    async def colour(self, ctx, argument):
        print(f"Recieved: >user update colour {ctx.author.name}")
        if len(argument) != 6:
            await ctx.send("Please use a valid hexadecimal colour value. uwu")
        else:
            doc_ref = dab.collection(str(ctx.author.id)).document('data')
            doc_ref.update({
                'colour':argument})
            await ctx.send("I've updated your colour, Senpai! >w<")
            print(f"{ctx.author.name} has updated their colour to {argument}")
            print('----------')

def setup(client):    
    client.add_cog(User(client))