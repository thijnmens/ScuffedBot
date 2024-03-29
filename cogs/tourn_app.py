from logging import info as logging_info, error as logging_error
from asyncio import TimeoutError

from discord import Embed, Colour
from firebase_admin import firestore

from discord.ext import commands


dab = firestore.client()
app_channel = (754631426263220244)
mod_app_channel = (804322542906638386)


class tourn_app(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, aliases=["app"])
    async def application(self, ctx):
        await ctx.message.delete()
        await ctx.send("Check your DMs, Senpai! >w<", delete_after=10)
        new = False
        col_ref = dab.collection('users').document('collectionlist').get().get('array')
        if str(ctx.author.id) not in col_ref:
            await ctx.author.send("What is your scoresaber link?")
            try:
                msg = await self.bot.wait_for('message', timeout=60, check=lambda message: message.author == ctx.author and message.guild is None)
                scoresaber = msg.content
            except TimeoutError:
                return await ctx.author.send("You didn't reply in time, please restart the process")
            scoresaber = scoresaber.split("?", 1)[0]
            scoresaber = scoresaber.split("&", 1)[0]
            doc_ref = dab.collection("users").document(str(ctx.author.id))
            doc_ref.set({
                'a': False,
                'chain_multi': 0,
                'username': ctx.author.name,
                'scoresaber': scoresaber
            })
            try:
                col_ref.append(str(ctx.author.id))
                col_ref.sort()
                dab.collection('users').document('collectionlist').update({'array': col_ref})
            except Exception as e:
                return logging_error(e+"\n----------")
            registered_role = await commands.RoleConverter().convert(ctx, "803577101906739270")
            await ctx.author.add_roles(registered_role)
            logging_info(f'Response: {ctx.author.name} has sucessfully been added to the database')
            new = True
        await ctx.author.send("What score did you get on ``Who's got Your Love - Stonebank``?")
        try:
            msg = await self.bot.wait_for('message', timeout=60, check=lambda message: message.author == ctx.author and message.guild is None)
            if msg.content.isdigit():
                love_score = int(msg.content)
            else:
                return await ctx.author.send("Only include numbers in your scores!\nPlease restart the process")
        except TimeoutError:
            return await ctx.author.send("You didn't reply in time, please restart the process")
        await ctx.author.send("Did you fail on ``Who's got Your Love - Stonebank``?\nPlease respond with __Yes__ or __No__\n**Respond with __Yes__ if you're playing on an older version than 1.13.2**")
        try:
            msg = await self.bot.wait_for('message', timeout=60, check=lambda message: message.author == ctx.author and message.guild is None)
            if msg.content.lower() == "no" or msg.content.lower() == "n":
                love_score = int(love_score / 2)
            elif msg.content.lower() == "yes" or msg.content.lower() == "y":
                True
            else:
                return await ctx.author.send("That's not a valid response!\nPlease restart the process")
        except TimeoutError:
            return await ctx.author.send("You didn't reply in time, please restart the process")
        await ctx.author.send("What score did you get on ``Himitsu Cult``?")
        try:
            msg = await self.bot.wait_for('message', timeout=60, check=lambda message: message.author == ctx.author and message.guild is None)
            if msg.content.isdigit():
                cult_score = int(msg.content)
            else:
                return await ctx.author.send("Only include numbers in your scores!\nPlease restart the process")
        except TimeoutError:
            return await ctx.author.send("You didn't reply in time, please restart the process")
        await ctx.author.send("Did you fail on ``Himitsu Cult``?\nPlease respond with __Yes__ or __No__\n**Respond with __Yes__ if you're playing on an older version than 1.13.2**")
        try:
            msg = await self.bot.wait_for('message', timeout=60, check=lambda message: message.author == ctx.author and message.guild is None)
            if msg.content.lower() == "no" or msg.content.lower() == "n":
                love_score = int(love_score / 2)
            elif not msg.content.lower() == "yes" or msg.content.lower() == "y":
                return await ctx.author.send("That's not a valid response!\nPlease restart the process")
        except TimeoutError:
            return await ctx.author.send("You didn't reply in time, please restart the process")
        await ctx.author.send("Can you post the link/links to your gameplay?\n\nIf you attach a video, make sure it's only one!")
        try:
            msg = await self.bot.wait_for('message', timeout=60, check=lambda message: message.author == ctx.author and message.guild is None)
            print(msg.attachments)
            if msg.attachments:
                video_link = getattr(msg.attachments[0], "url")
            else:
                video_link = msg.content
        except TimeoutError:
            return await ctx.author.send("You didn't reply in time, please restart the process")
        apps_count = (dab.collection("applications").document("count").get().get("val") + 1)
        dab.collection("applications").document("count").update({'val': apps_count})
        app_ref = dab.collection("applications").document(str(apps_count))
        total_score = int(love_score + cult_score)
        app_ref.set({
            'user_id': ctx.author.id,
            'love_score': love_score,
            'cult_score': cult_score,
            'total_score': total_score,
            'video_link': video_link,
            'status': "open"
        })
        if total_score >= 0 and total_score <= 200000:
            level = 1
        elif total_score >= 200001  and total_score <= 450000:
            level = 2
        elif total_score >= 450001  and total_score <= 700000:
            level = 3
        elif total_score >= 700001  and total_score <= 1100000:
            level = 4
        elif total_score >= 1100001  and total_score <= 1200000:
            level = 5
        elif total_score >= 1200001:
            level = "6 or 7"
        embed = Embed(
            title=f"Application ID: ``{apps_count}``",
            colour=Colour.green(),
            timestamp=ctx.message.created_at
        )
        if new is True:
            embed.add_field(
                name=f"{ctx.author.name} ({ctx.author.id})",
                value=f"[ScoreSaber]({scoresaber})",
                inline=True
            )
        else:
            scoresaber = dab.collection('users').document(str(ctx.author.id)).get().get('scoresaber')
            embed.add_field(
                name=f"{ctx.author.name} ({ctx.author.id})",
                value=f"[ScoreSaber]({scoresaber})",
                inline=True
            )
        embed.add_field(
            name="Scores",
            value=f"Who's Got Your Love?: ``{love_score}``\nHimitsu Cult: ``{cult_score}``\nTotal: ``{total_score}`` - Level {level}",
            inline=False
        )
        embed.add_field(
            name="Gameplay Footage",
            value=video_link,
            inline=True
        )
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await self.bot.get_channel(mod_app_channel).send(embed=embed)
        await ctx.author.send("Thank you! We'll ping you once we've determined your level")

    @application.command()
    async def id(self, ctx, arg1=None, *, arg2=None):
        if ctx.channel != mod_app_channel:
            return
        if arg1 or arg2 is None:
            return await ctx.send("args 1 and/or 2 are invalid\n``>app id <application id> <1-7 or decline reason>")
        app_ref = dab.collection("applications").document(str(arg1))
        app_user = self.bot.get_user(app_ref.get("user_id"))
        if arg2 == "1" or arg2 == "2" or arg2 == "3" or arg2 == "4" or arg2 == "5" or arg2 == "6" or arg2 == "7":
            await ctx.send(f"You're about to give {app_user.name} level {arg2}. Confirm?")
        else:
            await ctx.send(f"You're about to decline {app_user.name} with reason: ``{arg2}``. Confirm?")


def setup(bot):
    bot.add_cog(tourn_app(bot))
