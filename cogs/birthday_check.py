import discord
import os
import requests
import json
import firebase_admin
import asyncio
import logging
from datetime import datetime
from discord.ext import commands, tasks
from discord.utils import get
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db

client = discord.Client()
now = datetime.now()
current_time = now.strftime("%d-%m")
dab = firestore.client()


class birthday_check(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.birthdays.start()

    @tasks.loop(hours=12)
    async def birthdays(self):
        logging.info("Running birthdays")
        ref = dab.collection('collectionlist').document(
            'data').get().get('collectionarray')
        amount = len(ref)
        count = 0
        while (count < amount):
            try:
                ID = ref[count]
                try:
                    birthday = dab.collection(str(ID)).document('data').get().get('birthday')
                except Exception as e:
                    return logging.error(e)
                birthdaysplit = birthday.split('/')
                try:
                    birthdayfinal = birthdaysplit[0] + '-' + birthdaysplit[1]
                except Exception:
                    birthdayfinal = '32/13'
                current_time = now.strftime("%d-%m")
                a = dab.collection(str(ID)).document('data').get().get('a')
                if(birthdayfinal == current_time):
                    if(a == False):
                        channel = self.client.get_channel(793049781554642954)
                        await channel.send(f'<a:HyperTada:796323264888307731> Happy birthday <@!{ID}>! <a:HyperTada:796323264888307731>')
                        logging.info(f'Wished {ID} a happy birthday')
                        a = dab.collection(str(ID)).document('data').update({'a': True})
                    count = count + 1
            except Exception as e:
                logging.error(e)
        logging.info("Birthdays Ended\n----------")


def setup(client):
    client.add_cog(birthday_check(client))
