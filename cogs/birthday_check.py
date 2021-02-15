import discord
import logging
from datetime import datetime
from discord.ext import commands, tasks
from discord.utils import get
from firebase_admin import firestore

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
        ref = dab.collection('users').document('collectionlist').get().get('array')
        amount = len(ref) - 1
        count = 0
        while (count <= amount):
            try:
                ID = ref[count]
                try:
                    birthday = dab.collection("users").document(str(ID)).get().get('birthday')
                except Exception:
                    count = count + 1
                    logging.info(f'The user with id {ID} did not add his b-day to the database yet')
                    continue
                birthdaysplit = birthday.split('/')
                try:
                    birthdayfinal = birthdaysplit[0] + '-' + birthdaysplit[1]
                except Exception:
                    birthdayfinal = '32/13'
                current_time = now.strftime("%d-%m")
                a = dab.collection("users").document(str(ID)).get().get('a')
                if(birthdayfinal == current_time):
                    if(a == False):
                        channel = self.client.get_channel(793049781554642954)
                        await channel.send(f'<a:HyperTada:796323264888307731> Happy birthday <@!{ID}>! <a:HyperTada:796323264888307731>')
                        logging.info(f'Wished {ID} a happy birthday')
                        dab.collection("users").document(str(ID)).update({'a': True})
            except Exception as e:
                logging.error(e)
            count = count + 1
        logging.info("Birthdays Ended\n----------")


def setup(client):
    client.add_cog(birthday_check(client))
