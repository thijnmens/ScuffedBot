import discord
import os
import logging
from discord.ext import commands, tasks
from discord.utils import get
from firebase_admin import credentials, firestore, db

dab = firestore.client()
chain_channel = (803259546390888458)

class chain_enforcement(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener('on_message')
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        if message.channel.id != chain_channel:
            return
        logging.info("chain_enforcement triggered")
        current_chain_message = dab.collection(str("chain_data")).document("chain_data").get().get("message")
        current_chain_lenght = dab.collection(str("chain_data")).document("chain_data").get().get("lenght")
        muted_list = dab.collection(str("chain_data")).document("muted").get().get("muted")
        ref = dab.collection(str("chain_data")).document('muted')
        if message.content != current_chain_message:
            channel = self.client.get_channel(803259546390888458)
            await channel.send(f'The chain had {current_chain_lenght} messages')
            member = message.author
            await message.add_roles('Muted')
            muted_list = muted_list.append(member)
            ref.update({'muted': muted_list})
        else:
            lenght = current_chain_lenght + 1
            dab.collection(str("chain_data")).document('chain_data').update({'lenght': lenght})

    @tasks.loop(seconds=10)
    async def mutedcheck(self):
        muted_list = dab.collection(str("chain_data")).document("muted").get().get("muted")
        amount = len(muted_list)
        a = 0
        if a < amount:
            print(muted_list[a])
            a = a + 1

def setup(client):
    client.add_cog(chain_enforcement(client))
