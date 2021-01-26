import discord
import os
import logging
import asyncio
from discord.ext import commands, tasks
from discord.utils import get
from firebase_admin import credentials, firestore, db

dab = firestore.client()
chain_channel = (803259546390888458)
muted = set()


async def mute(ctx, current_chain_lenght):
    mute_role = await commands.RoleConverter().convert(ctx, 783042590739529789)
    time = int(current_chain_lenght * 10)
    muted.add(ctx.author.id)
    await ctx.add_roles(mute_role)
    logging.info(f"{ctx.author.id} placed in muted\n{muted}")
    await asyncio.sleep(time)
    muted.remove(ctx.author.id)
    await ctx.remove_roles(mute_role)
    logging.info(f"{ctx.author.id} removed from muted\n{muted}")


class chain_enforcement(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener('on_message')
    async def on_message(self, ctx):
        if ctx.author == self.client.user:
            return
        if ctx.channel.id != chain_channel:
            return
        logging.info("chain_enforcement triggered")
        current_chain_message = dab.collection(str("chain_data")).document("chain_data").get().get("message")
        current_chain_lenght = dab.collection(str("chain_data")).document("chain_data").get().get("lenght")
        if ctx.content != current_chain_message:
            if current_chain_lenght != 0:
                channel = self.client.get_channel(chain_channel)
                await channel.send(f'The chain had {current_chain_lenght} messages')
                mute(ctx, current_chain_lenght)
                dab.collection(str("chain_data")).document("chain_data").update({'message': ctx.content})
                dab.collection(str("chain_data")).document('chain_data').update({'lenght': 0})
        else:
            lenght = current_chain_lenght + 1
            dab.collection(str("chain_data")).document('chain_data').update({'lenght': lenght})

def setup(client):
    client.add_cog(chain_enforcement(client))
