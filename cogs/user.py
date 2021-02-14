import discord
import asyncio
import re
import logging
from discord.ext import commands
from discord.utils import get
from firebase_admin import firestore

dab = firestore.client()


class user(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.valid_HMD = [
            "CV1",
            "Rift S",
            "Quest",
            "Quest 2",
            "Index",
            "Vive",
            "WMR"]


    # User
    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=["u"])
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
        logging.info(f'Recieved: >user {ctx.author.name}')
        ref = dab.collection("users").document(str(ctx.author.id)).get()
        username = ref.get("username")
        if username is None:
            logging.info(f"User not found")
            if argument is None:
                return await ctx.send("You're not in my database, Senpai! qwq\nYou should use ``>user add`` <w<")
            elif argument is not None:
                return await ctx.send("That person isn't in my database qwq")
        scoresaber = ref.get("scoresaber")
        try:
            steam = ref.get("steam")
        except BaseException:
            steam = None
        try:
            twitch = ref.get("twitch")
        except BaseException:
            twitch = None
        try:
            youtube = ref.get("youtube")
        except BaseException:
            youtube = None
        try:
            twitter = ref.get("twitter")
        except BaseException:
            twitter = None
        try:
            reddit = ref.get("reddit")
        except BaseException:
            reddit = None
        try:
            hmd = ref.get("hmd")
        except BaseException:
            hmd = None
        try:
            birthday = ref.get("birthday")
        except BaseException:
            birthday = None
        try:
            pfp = ref.get("pfp")
        except BaseException:
            pfp = None
        try:
            status = ref.get("status")
        except BaseException:
            status = None
        # try:
        #   this on for size, Mister
        links_Message = f"[Scoresaber]({scoresaber}) "
        if steam is not None:
            links_Message = links_Message + f"| [Steam]({steam}) "
        if twitch is not None:
            links_Message = links_Message + f"| [Twitch]({twitch}) "
        if youtube is not None:
            links_Message = links_Message + f"| [Youtube]({youtube}) "
        if twitter is not None:
            links_Message = links_Message + f"| [Twitter]({twitter}) "
        if reddit is not None:
            links_Message = links_Message + f"| [Reddit]({reddit}) "
        try:
            colourRaw = ref.get("colour")
            colour = await commands.ColourConverter().convert(ctx, colourRaw)
            embed = discord.Embed(title=username, colour=colour)
        except Exception as e:
            embed = discord.Embed(
                title=username,
                colour=discord.Colour.random())
            logging.warning(f"Funny colour exception: {e}")
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
        logging.info('Response: user embed\n----------')

    # User Add
    @user.command()
    async def add(self, ctx, argument=None):
        logging.info(f'Recieved: >user add {ctx.author.name}')
        if ctx.guild is None:
            logging.info("ctx.guild is None\n----------")
            return await ctx.send("Please only use this command within the Scuffed Tourneys server! >w<")
        col_ref = dab.collection('users').document('collectionlist').get().get('array')
        if str(ctx.author.id) in col_ref:
            return await ctx.send("Baka! You're already in the database!\nUse ``>user update`` instead")
        elif argument is None:
            sent = await ctx.send('What is your scoresaber link?')
            try:
                msg = await self.client.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
                scoresaber = msg.content
            except asyncio.TimeoutError:
                await sent.delete()
                return await ctx.send("You didn't reply in time, please restart the process")
        elif argument is not None:
            scoresaber = argument
        if scoresaber.isdigit():
            scoresaber = "https://scoresaber.com/u/"+scoresaber
        else:
            scoresaber = scoresaber.split("?", 1)[0]
            scoresaber = scoresaber.split("&", 1)[0]
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.set({
            'a': False,
            'chain_multi': 0,
            'username': ctx.author.name,
            'scoresaber': scoresaber,
            'bal': 0,
            'inv': []
        })
        try:
            col_ref.append(str(ctx.author.id))
            col_ref.sort()
            dab.collection('users').document('collectionlist').update({'array': col_ref})
        except Exception as e:
            return logging.error(e+"\n----------")
        registered_role = await commands.RoleConverter().convert(ctx, "803577101906739270")
        await ctx.author.add_roles(registered_role)
        await ctx.send(f'{ctx.author.name} has sucessfully been added to the database!\nUse ``>user update`` to add optional customisation')
        logging.info(f'Response: {ctx.author.name} has sucessfully been added to the database\n----------')

    # User Remove
    @user.command()
    async def remove(self, ctx):
        logging.info(f"User remove ran by {ctx.author.name}")
        if ctx.guild is None:
            logging.info("ctx.guild is None\n----------")
            return await ctx.send("Please only use this command within the Scuffed Tourneys server! >w<")
        try:
            col_ref = dab.collection('users').document('collectionlist').get().get('array')
            col_ref.remove(str(ctx.author.id))
            dab.collection('users').document('collectionlist').update({'array': col_ref})
            dab.collection("users").document(str(ctx.author.id)).delete()
            registered_role = await commands.RoleConverter().convert(ctx, "803577101906739270")
            await ctx.author.remove_roles(registered_role)
            await ctx.send(f"{ctx.author.name} has been successfully removed from the database")
            logging.info(f"Response: {ctx.author.id} has been successfully removed to the database\n----------")
        except Exception as e:
            logging.error(e+"\n----------")
    
    @commands.Cog.listener("on_member_remove")
    async def on_member_remove(self, member):
        logging.info(f"{member.name} ({member.id}) has left the server")
        try:
            col_ref = dab.collection('users').document('collectionlist').get().get('array')
            col_ref.remove(str(member.id))
            dab.collection('users').document('collectionlist').update({'array': col_ref})
            dab.collection("users").document(str(member.id)).delete()
            await self.client.get_channel(754625185306378271).send(f"{member.name} ({member.id}) has left the server and been successfully removed from the database")
            logging.info(f"Response: {member.id} has been successfully removed to the database\n----------")
        except Exception as e:
            logging.error(e)

    # User update
    @user.group(invoke_without_command=True, case_insensitive=True)
    async def update(self, ctx):
        logging.info(f"Recieved: >user update")
        await ctx.send("B-Baka!! You need to tell me what you want to update!!\nUse ``>help update`` to check the valid arguments")
        logging.info("no sub command given\n---------")

    @update.command()
    async def username(self, ctx, *, argument):
        logging.info(f'Recieved: >user update username {ctx.author.name}')
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({'username': argument})
        await ctx.send(f"I've updated Senpai's username to {argument}! >w<")
        logging.info(f"{ctx.author.name} has updated their username to {argument}\n----------")

    @update.command()
    async def scoresaber(self, ctx, argument):
        logging.info(f'Recieved: >user update scoresaber {ctx.author.name}')
        if argument.isdigit():
            argument = "https://scoresaber.com/u/"+argument
        else:
            argument = argument.split("?", 1)[0]
            argument = argument.split("&", 1)[0]
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            'scoresaber': argument})
        await ctx.send("I've updated your Scoresaber, Senpai! >w<")
        logging.info(f"{ctx.author.name} has updated their scoresaber to {argument}\n----------")

    @update.command()
    async def steam(self, ctx, argument):
        logging.info(f'Recieved: >user update steam {ctx.author.name}')
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            'steam': argument})
        await ctx.send("I've updated your Steam, Senpai! >w<")
        logging.info(f"{ctx.author.name} has updated their steam to {argument}\n----------")

    @update.command()
    async def twitch(self, ctx, argument):
        logging.info(f'Recieved: >user update twitch {ctx.author.name}')
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            'twitch': argument})
        await ctx.send("I've updated your Twitch, Senpai! >w<")
        logging.info(f"{ctx.author.name} has updated their twitch to {argument}\n----------")

    @update.command()
    async def youtube(self, ctx, argument):
        logging.info(f'Recieved: >user update youtube {ctx.author.name}')
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            'youtube': argument})
        await ctx.send("I've updated your Youtube, Senpai! >w<")
        logging.info(f"{ctx.author.name} has updated their youtube to {argument}\n----------")

    @update.command()
    async def twitter(self, ctx, argument):
        logging.info(f'Recieved: >user update twitter {ctx.author.name}')
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            'twitter': argument})
        await ctx.send("I've updated your Twitter, Senpai! >w<")
        logging.info(f"{ctx.author.name} has updated their twitter to {argument}\n----------")

    @update.command()
    async def reddit(self, ctx, argument):
        logging.info(f'Recieved: >user update reddit {ctx.author.name}')
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            'reddit': argument})
        await ctx.send("I've updated your Reddit, Senpai! >w<")
        logging.info(f"{ctx.author.name} has updated their reddit to {argument}\n----------")

    @update.command()
    async def birthday(self, ctx, argument):
        logging.info(f'Recieved: >user update birthday {ctx.author.name}')
        if ((bool(re.search(r"\d/", argument)))) is False:
            logging.warning("Birthday input validation triggered")
            await ctx.send("Oopsie, looks like you did a woopsie! uwu\n``Don't use characters expect for numbers and /``")
            return
        storer = argument.split('/')
        storer[0] = int(storer[0])
        storer[1] = int(storer[1])
        if(storer[1] > 12 or storer[1] < 1 or storer[0] > 31 or storer[0] < 1):
            logging.warning("Birthday legitimacy triggered")
            return await ctx.send("B-Baka!! that date doesn't make any sense!\n``Please use a legitimate date``")
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            'birthday': argument})
        await ctx.send(f"I've updated Senpai's birthday to {argument}! >w<")
        logging.info(f"{ctx.author.name} has updated their birthday to {argument}\n----------")

    @update.command()
    async def hmd(self, ctx, *, argument):
        logging.info(f'Recieved: >user update hmd {ctx.author.name}')
        valid_HMD_low = [x.lower() for x in self.client.valid_HMD]
        try:
            pos = valid_HMD_low.index(argument.lower()) 
        except:
            logging.warning(f"{argument} not in valid_HMD")
            return await ctx.send("BAKA!! That HMD isn't valid!\n``Use >help update to check the valid HMDs``")
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            'hmd': self.client.valid_HMD[pos]})
        await ctx.send(f"I've updated Senpai's HMD to {self.client.valid_HMD[pos]}! >w<")
        logging.info(f"{ctx.author.name} has updated their status to {self.client.valid_HMD[pos]}\n----------")

    @update.command()
    async def pfp(self, ctx, argument):
        logging.info(f"Recieved: >user update pfp {ctx.author.name}")
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            'pfp': argument})
        await ctx.send("I've updated your pfp, Senpai! >w<")
        logging.info(f"{ctx.author.name} has updated their pfp to {argument}\n----------")

    @update.command()
    async def status(self, ctx, *, argument):
        logging.info(f'Recieved: >user update status {ctx.author.name}')
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            'status': argument})
        await ctx.send("I've updated your status, Senpai! >w<")
        logging.info(f"{ctx.author.name} has updated their status to {argument}\n----------")

    @update.command(aliases=["color"])  # Americans ew
    async def colour(self, ctx, argument):
        logging.info(f"Recieved: >user update colour {ctx.author.name}")
        try:
            await commands.ColourConverter().convert(ctx, argument)
        except Exception as e:
            await ctx.send("Please use a valid hexadecimal colour value. uwu")
            return logging.error(f"expect triggered: {e}")
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            'colour': argument})
        await ctx.send("I've updated your colour, Senpai! >w<")
        logging.info(f"{ctx.author.name} has updated their colour to {argument}\n----------")


def setup(client):
    client.add_cog(user(client))
