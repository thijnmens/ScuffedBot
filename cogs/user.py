import discord
import asyncio
import re
import logging
from discord.ext import commands
from discord.utils import get
from firebase_admin import firestore

dab = firestore.client()


class user(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.valid_HMD = [
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
                ctx.author = self.bot.get_user(int(argument))
                if ctx.author is None:
                    return await ctx.send("Sorry Senpai, I can't find anyone with that ID qwq")
            else:
                ID = argument[3:]
                ID = ID[:-1]
                ctx.author = self.bot.get_user(int(ID))
        logging.info(f'Recieved user {ctx.author.name}')
        ref = dab.collection("users").document(str(ctx.author.id)).get()
        if ref.exists is False:
            logging.info(f"User not found")
            if argument is None:
                return await ctx.send("You're not in my database, Senpai! qwq\nYou should use ``>user add`` <w<")
            elif argument is not None:
                return await ctx.send("That person isn't in my database qwq")
        username = ref.get("username")
        scoresaber = ref.get("scoresaber")
        links_Message = f"[Scoresaber]({scoresaber}) "
        try:
            steam = ref.get("steam")
            links_Message = links_Message + f"| [Steam]({steam}) "
        except BaseException:
            True
        try:
            twitch = ref.get("twitch")
            links_Message = links_Message + f"| [Twitch]({twitch}) "
        except BaseException:
            True
        try:
            youtube = ref.get("youtube")
            links_Message = links_Message + f"| [Youtube]({youtube}) "
        except BaseException:
            True
        try:
            twitter = ref.get("twitter")
            links_Message = links_Message + f"| [Twitter]({twitter}) "
        except BaseException:
            True
        try:
            reddit = ref.get("reddit")
            links_Message = links_Message + f"| [Reddit]({reddit}) "
        except BaseException:
            True
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
        #hilarious
        try:
            colourRaw = ref.get("colour")
            colour = await commands.ColourConverter().convert(ctx, "0x"+colourRaw)
            embed = discord.Embed(title=username, colour=colour)
        except BaseException:
            embed = discord.Embed(
                title=username,
                colour=discord.Colour.random())
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
    @user.command(case_insensitive=True)
    async def add(self, ctx, argument=None):
        logging.info(f'Recieved user add {ctx.author.name}')
        if ctx.guild is None:
            logging.info("ctx.guild is None\n----------")
            return await ctx.send("Please only use this command within the Scuffed Tourneys server! >w<")
        col_ref = dab.collection('users').document('collectionlist').get().get('array')
        if str(ctx.author.id) in col_ref:
            return await ctx.send("Baka! You're already in the database!\nUse ``>user update`` instead")
        elif argument is None:
            sent = await ctx.send('What is your scoresaber link?')
            try:
                msg = await self.bot.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
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
            'wished': False,
            'chain_multi': 0,
            'username': ctx.author.name,
            'scoresaber': scoresaber,
            'bal': 0,
            'bank': 666,
            'inv': ['gun~0', 'friend~0']
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
    
    @commands.Cog.listener("on_member_remove")
    async def on_member_remove(self, member):
        logging.info(f"{member.name} ({member.id}) has left the server")
        try:
            col_ref = dab.collection('users').document('collectionlist').get().get('array')
            col_ref.remove(str(member.id))
            dab.collection('users').document('collectionlist').update({'array': col_ref})
            dab.collection("users").document(str(member.id)).delete()
            await self.bot.get_channel(754625185306378271).send(f"{member.name} ({member.id}) has left the server and been successfully removed from the database")
            logging.info(f"Response: {member.id} has been successfully removed to the database\n----------")
        except Exception as e:
            logging.error(e)

    # User Remove
    @user.group(invoke_without_command=True, case_insensitive=True)
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

    @remove.command(case_insensitive=True, aliases=["username"])
    async def remove_username(self, ctx):
        logging.info(f"Recieved: user remove username {ctx.author.name}")
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            "username": ctx.author.name
        })
        await ctx.send("I've removed Senpai's username >w<")
        logging.info(f"{ctx.author.name} has removed their username")

    @remove.command(case_insensitive=True, aliases=["steam"])
    async def remove_steam(self, ctx):
        logging.info(f"Recieved: user remove Steam {ctx.author.name}")
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            "steam": firestore.DELETE_FIELD
        })
        await ctx.send("I've removed Senpai's Steam >w<")
        logging.info(f"{ctx.author.name} has removed their Steam")

    @remove.command(case_insensitive=True, aliases=["twitch"])
    async def remove_twitch(self, ctx):
        logging.info(f"Recieved: user remove Twitch {ctx.author.name}")
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            "twitch": firestore.DELETE_FIELD
        })
        await ctx.send("I've removed Senpai's Twitch >w<")
        logging.info(f"{ctx.author.name} has removed their Twitch")

    @remove.command(case_insensitive=True, aliases=["youtube"])
    async def remove_youtube(self, ctx):
        logging.info(f"Recieved: user remove Youtube {ctx.author.name}")
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            "youtube": firestore.DELETE_FIELD
        })
        await ctx.send("I've removed Senpai's Youtube >w<")
        logging.info(f"{ctx.author.name} has removed their Youtube")

    @remove.command(case_insensitive=True, aliases=["twitter"])
    async def remove_twitter(self, ctx):
        logging.info(f"Recieved: user remove Twitter {ctx.author.name}")
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            "twitter": firestore.DELETE_FIELD
        })
        await ctx.send("I've removed Senpai's Twitter >w<")
        logging.info(f"{ctx.author.name} has removed their Twitter")

    @remove.command(case_insensitive=True, aliases=["reddit"])
    async def remove_reddit(self, ctx):
        logging.info(f"Recieved: user remove Reddit {ctx.author.name}")
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            "reddit": firestore.DELETE_FIELD
        })
        await ctx.send("I've removed Senpai's Reddit >w<")
        logging.info(f"{ctx.author.name} has removed their Reddit")

    @remove.command(case_insensitive=True, aliases=["birthday"])
    async def remove_birthday(self, ctx):
        logging.info(f"Recieved: user remove birthday {ctx.author.name}")
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            "birthday": firestore.DELETE_FIELD
        })
        await ctx.send("I've removed Senpai's Birthday >w<")
        logging.info(f"{ctx.author.name} has removed their Birthday")

    @remove.command(case_insensitive=True, aliases=["hmd"])
    async def remove_hmd(self, ctx):
        logging.info(f"Recieved: user remove HMD {ctx.author.name}")
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            "hmd": firestore.DELETE_FIELD
        })
        await ctx.send("I've removed Senpai's HMD >w<")
        logging.info(f"{ctx.author.name} has removed their HMD")

    @remove.command(case_insensitive=True, aliases=["pfp"])
    async def remove_pfp(self, ctx):
        logging.info(f"Recieved: user remove pfp {ctx.author.name}")
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            "pfp": firestore.DELETE_FIELD
        })
        await ctx.send("I've removed Senpai's pfp >w<")
        logging.info(f"{ctx.author.name} has removed their pfp")

    @remove.command(case_insensitive=True, aliases=["status"])
    async def remove_status(self, ctx):
        logging.info(f"Recieved: user remove status {ctx.author.name}")
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            "status": firestore.DELETE_FIELD
        })
        await ctx.send("I've removed Senpai's status >w<")
        logging.info(f"{ctx.author.name} has removed their status")

    @remove.command(case_insensitive=True, aliases=["colour", "color"])
    async def remove_colour(self, ctx):
        logging.info(f"Recieved: user remove colour {ctx.author.name}")
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            "colour": firestore.DELETE_FIELD
        })
        await ctx.send("I've removed Senpai's colour >w<")
        logging.info(f"{ctx.author.name} has removed their colour")
    
    # User update
    @user.group(invoke_without_command=True, case_insensitive=True)
    async def update(self, ctx):
        logging.info(f"Recieved user update")
        await ctx.send("B-Baka!! You need to tell me what you want to update!!\nUse ``>help update`` to check the valid arguments")
        logging.info("no sub command given\n---------")

    @update.command(case_insensitive=True)
    async def username(self, ctx, *, argument):
        logging.info(f'Recieved user update username {ctx.author.name}')
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({'username': argument})
        await ctx.send(f"I've updated Senpai's username to {argument}! >w<")
        logging.info(f"{ctx.author.name} has updated their username to {argument}\n----------")

    @update.command(case_insensitive=True)
    async def scoresaber(self, ctx, argument):
        logging.info(f'Recieved user update scoresaber {ctx.author.name}')
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

    @update.command(case_insensitive=True)
    async def steam(self, ctx, argument):
        logging.info(f'Recieved user update steam {ctx.author.name}')
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            'steam': argument})
        await ctx.send("I've updated your Steam, Senpai! >w<")
        logging.info(f"{ctx.author.name} has updated their steam to {argument}\n----------")

    @update.command(case_insensitive=True)
    async def twitch(self, ctx, argument):
        logging.info(f'Recieved user update twitch {ctx.author.name}')
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            'twitch': argument})
        await ctx.send("I've updated your Twitch, Senpai! >w<")
        logging.info(f"{ctx.author.name} has updated their twitch to {argument}\n----------")

    @update.command(case_insensitive=True)
    async def youtube(self, ctx, argument):
        logging.info(f'Recieved user update youtube {ctx.author.name}')
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            'youtube': argument})
        await ctx.send("I've updated your Youtube, Senpai! >w<")
        logging.info(f"{ctx.author.name} has updated their youtube to {argument}\n----------")

    @update.command(case_insensitive=True)
    async def twitter(self, ctx, argument):
        logging.info(f'Recieved user update twitter {ctx.author.name}')
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            'twitter': argument})
        await ctx.send("I've updated your Twitter, Senpai! >w<")
        logging.info(f"{ctx.author.name} has updated their twitter to {argument}\n----------")

    @update.command(case_insensitive=True)
    async def reddit(self, ctx, argument):
        logging.info(f'Recieved user update reddit {ctx.author.name}')
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            'reddit': argument})
        await ctx.send("I've updated your Reddit, Senpai! >w<")
        logging.info(f"{ctx.author.name} has updated their reddit to {argument}\n----------")

    @update.command(case_insensitive=True)
    async def birthday(self, ctx, argument):
        logging.info(f'Recieved user update birthday {ctx.author.name}')
        if ((bool(re.search(r"\d/", argument)))) is False:
            logging.warning("Birthday input validation triggered")
            await ctx.send("Oopsie, looks like you did a woopsie! uwu\n``Don't use characters expect for numbers and /``")
            return
        storer = argument.split('/')
        storer[0] = int(storer[0])
        storer[1] = int(storer[1])
        if(storer[1] > 12 or storer[1] < 1 or storer[0] > 31 or storer[0] < 1):
            logging.warning("Birthday legitimacy triggered, date and/or month invalid")
            return await ctx.send("B-Baka!! that date doesn't make any sense!\n``Please use a legitimate date``")
        try: 
            print(int(len(storer[2])))
            if int(len(storer[2])) > 4 or int(len(storer[2])) < 4:
                logging.warning("Birthday legitmacy triggered, year invalid")
                return await ctx.send("B-Baka!! that date doesn't make any sense!\n``Please use a legitimate year, or don't include one``")
        except IndexError:
            False
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            'birthday': argument})
        await ctx.send(f"I've updated Senpai's birthday to {argument}! >w<")
        logging.info(f"{ctx.author.name} has updated their birthday to {argument}\n----------")

    @update.command(case_insensitive=True)
    async def hmd(self, ctx, *, argument):
        logging.info(f'Recieved user update hmd {ctx.author.name}')
        valid_HMD_low = [x.lower() for x in self.bot.valid_HMD]
        try:
            pos = valid_HMD_low.index(argument.lower()) 
        except:
            logging.warning(f"{argument} not in valid_HMD")
            return await ctx.send("BAKA!! That HMD isn't valid!\n``Use >help update to check the valid HMDs``")
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            'hmd': self.bot.valid_HMD[pos]})
        await ctx.send(f"I've updated Senpai's HMD to {self.bot.valid_HMD[pos]}! >w<")
        logging.info(f"{ctx.author.name} has updated their status to {self.bot.valid_HMD[pos]}\n----------")

    @update.command(case_insensitive=True)
    async def pfp(self, ctx, argument):
        logging.info(f"Recieved user update pfp {ctx.author.name}")
        if argument[:4] != "http":
            logging.warning(f"Argument is not a link ({argument})")
            return await ctx.send("Baka! You can only use links for your profile picture!")
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            'pfp': argument})
        await ctx.send("I've updated your pfp, Senpai! >w<")
        logging.info(f"{ctx.author.name} has updated their pfp to {argument}\n----------")

    @update.command(case_insensitive=True)
    async def status(self, ctx, *, argument):
        logging.info(f'Recieved user update status {ctx.author.name}')
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            'status': argument})
        await ctx.send("I've updated your status, Senpai! >w<")
        logging.info(f"{ctx.author.name} has updated their status to {argument}\n----------")

    @update.command(aliases=["color"])  # Americans ew
    async def colour(self, ctx, argument):
        logging.info(f"Recieved user update colour {ctx.author.name}")
        try:
            await commands.ColourConverter().convert(ctx, "0x"+argument)
        except Exception as e:
            await ctx.send("Please use a valid hexadecimal colour value. uwu")
            return logging.error(f"expect triggered: {e}")
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            'colour': argument})
        await ctx.send("I've updated your colour, Senpai! >w<")
        logging.info(f"{ctx.author.name} has updated their colour to {argument}\n----------")


def setup(bot):
    bot.add_cog(user(bot))
