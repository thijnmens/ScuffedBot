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
        ref = dab.collection(str("chain_data")).document("chain_data").get()
        current_chain_message = ref.get("message")
        if message.content != current_chain_message:
            await message.delete()

def setup(client):
    client.add_cog(chain_enforcement(client))
