import discord
import logging
from discord.ext import commands
from discord.utils import get
from firebase_admin import firestore

dab = firestore.client()

class items(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=["s"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def use(self, ctx):
        logging.info('Recieved: >use')
        logging.info('Response: nothing\n----------')

def setup(client):
    client.add_cog(items(client))