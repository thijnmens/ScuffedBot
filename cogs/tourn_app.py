import discord
import logging
import asyncio
from discord.ext import commands
from discord.utils import get
from firebase_admin import credentials, firestore, db

dab = firestore.client()
app_channel = (754631426263220244)
mod_app_channel = (804322542906638386)


class tourn_app(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(case_insensitive=True, aliases=["app"])
    async def application(self, ctx):
        logging.info(f'Recieved: >application: {ctx.author.name}')
        await ctx.message.delete()
        await ctx.send("Check your DMs, Senpai! >w<", delete_after=10)
        new = False
        col_ref = dab.collection('users').document('collectionlist').get().get('array')
        if str(ctx.author.id) not in col_ref:
            await ctx.author.send("What is your scoresaber link?")
            try:
                msg = await self.client.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author and message.guild is None)
                scoresaber = msg.content
            except asyncio.TimeoutError:
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
                return logging.error(e+"\n----------")
            registered_role = await commands.RoleConverter().convert(ctx, "803577101906739270")
            await ctx.author.add_roles(registered_role)
            logging.info(f'Response: {ctx.author.name} has sucessfully been added to the database\n----------')
            new = True
        await ctx.author.send("What score did you get on ``Who's got Your Love - Stonebank``?")
        try:
            msg = await self.client.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author and message.guild is None)
            if msg.content.isdigit():
                love_score = int(msg.content)
            else:
                return await ctx.author.send("Only include numbers in your scores!\nPlease restart the process")
        except asyncio.TimeoutError:
            return await ctx.author.send("You didn't reply in time, please restart the process")
        await ctx.author.send("What score did you get on ``Himitsu Cult``?")
        try:
            msg = await self.client.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author and message.guild is None)
            if msg.content.isdigit():
                cult_score = int(msg.content)
            else:
                return await ctx.author.send("Only include numbers in your scores!\nPlease restart the process")
        except asyncio.TimeoutError:
            return await ctx.author.send("You didn't reply in time, please restart the process")
        await ctx.author.send("Can you post the link/links to your gameplay?")
        try:
            msg = await self.client.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author and message.guild is None)
            video_link = msg.content
        except asyncio.TimeoutError:
            return await ctx.author.send("You didn't reply in time, please restart the process")
        apps_count = (dab.collection("applications").document("count").get().get("val") + 1)
        dab.collection("applications").document("count").update({'val': apps_count})
        app_ref = dab.collection("applications").document(str(apps_count))
        app_ref.set({
            'user_id': ctx.author.id,
            'love_score': love_score,
            'cult_score': cult_score,
            'video_link': video_link,
            'status': "open"
        })
        embed = discord.Embed(
            title=f"Application ID: ``{apps_count}``",
            colour=discord.Colour.green(),
            timestamp=ctx.message.created_at
        )
        if new is True:
            embed.add_field(
                name=ctx.author.name,
                value=f"{ctx.atuhor.id}\n[scoresaber]({scoresaber})",
                inline=True
            )
        else:
            scoresaber = dab.collection('users').document(str(ctx.author.id)).get().get('scoresaber')
            embed.add_field(
                name=ctx.author.name,
                value=f"{ctx.atuhor.id}\n[scoresaber]({scoresaber})",
                inline=True
            )
        embed.add_field(
            name="Who's Got Your Love?",
            value=love_score,
            inline=False
        )
        embed.add_field(
            name="Himitsu Cult",
            value=cult_score,
            inline=False
        )
        embed.add_field(
            name="Gameplay Footage",
            value=video_link,
            inline=True
        )
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await self.client.get_channel(mod_app_channel).send(embed=embed)
        await ctx.author.send("Thank you! We'll ping you once we've determined your level")
        logging.info("application finished and sent to #applications\n---------")

def setup(client):
    client.add_cog(tourn_app(client))
