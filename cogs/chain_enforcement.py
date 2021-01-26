import discord
import os
import logging
import asyncio
from discord.ext import commands, tasks
from discord.utils import get
from firebase_admin import credentials, firestore, db

dab = firestore.client()
chain_channel = (796012513917272085)


async def mute(message, time):
    mute_role = await commands.RoleConverter().convert(message, "783042590739529789")
    await message.author.add_roles(mute_role)
    logging.info(f"{message.author.id} placed in muted for: {time} seconds")
    await asyncio.sleep(time)
    await message.author.remove_roles(mute_role)
    logging.info(f"{message.author.id} removed from muted")


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
        if message.content != current_chain_message:
            if current_chain_lenght != 0:
                channel = self.client.get_channel(chain_channel)
                time = int(current_chain_lenght * 10)
                await channel.send(f'The chain had {current_chain_lenght} messages. {message.author.name} has been muted for {time} seconds!\nThe new chain message is: {message.content}')
                dab.collection(str("chain_data")).document("chain_data").update({'message': message.content})
                dab.collection(str("chain_data")).document('chain_data').update({'lenght': 0})
                await mute(message, current_chain_lenght)
        else:
            lenght = current_chain_lenght + 1
            dab.collection(str("chain_data")).document('chain_data').update({'lenght': lenght})

def setup(client):
    client.add_cog(chain_enforcement(client))
