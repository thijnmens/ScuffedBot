import discord
import os
import logging
import asyncio
from discord.ext import commands
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
        if message.valid is True:
            return
        if message.channel.id != chain_channel:
            return
        logging.info("chain_enforcement running")
        if message.attachments:
            await message.delete()
            return logging.info("Message contained attachment and has been deleted. chain_enforcement ended\n---------")
        current_chain_message = dab.collection(str("chain_data")).document("chain_data").get().get("message")
        current_chain_length = dab.collection(str("chain_data")).document("chain_data").get().get("length")
        chain_multi = dab.collection("users").document(str(message.author.id)).get().get("chain_multi")
        if message.content != current_chain_message:
            logging.info("chain_enforcement triggered")
            channel = self.client.get_channel(chain_channel)
            time = float(float(current_chain_length) * 10.0 * chain_multi)
            await channel.send(f'The chain lasted {current_chain_length} messages. {message.author.name} has been muted for {time} seconds!\nThe new chain message is: {message.content}')
            dab.collection(str("chain_data")).document("chain_data").update({
                'message': message.content,
                'length': 1
            })
            dab.collection("users").document(str(message.author.id)).update({"chain_multi": float(chain_multi+0.5)})
            await mute(message, time)
        else:
            dab.collection(str("chain_data")).document('chain_data').update({'length': int(current_chain_length + 1)})
        logging.info("chain_enforcement ran\n---------")

def setup(client):
    client.add_cog(chain_enforcement(client))
