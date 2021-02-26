import logging
from datetime import datetime
from discord.ext import commands, tasks
from discord.utils import get
from firebase_admin import firestore

current_time = datetime.now().strftime("%d-%m")
dab = firestore.client()


class birthday_check(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.birthdays.start()

    @tasks.loop(hours=12)
    async def birthdays(self):
        await self.bot.wait_until_ready()
        logging.info("Running birthdays")
        ref = dab.collection('users').document('collectionlist').get().get('array')
        amount = len(ref) - 1
        count = 0
        while (count <= amount):
            try:
                ID = ref[count]
                try:
                    birthday = dab.collection("users").document(str(ID)).get().get('birthday')
                except Exception as e:
                    e = str(e)
                    count = count + 1
                    if e.find('is not contained in the data') != -1:
                        logging.info(f'user {ID} hasn\'t saved their birthday to the database')
                    else:
                        logging.error(f'{ID}: {e}')
                    continue
                birthdaysplit = birthday.split('/')
                try:
                    birthdayfinal = birthdaysplit[0] + '-' + birthdaysplit[1]
                except Exception:
                    birthdayfinal = '32/13'
                a = dab.collection("users").document(str(ID)).get().get('a')
                if(birthdayfinal == current_time):
                    if(a == False):
                        await self.bot.get_channel(793049781554642954).send(f'<a:HyperTada:796323264888307731> Happy birthday <@!{ID}>! <a:HyperTada:796323264888307731>')
                        logging.info(f'Wished {ID} a happy birthday')
                        dab.collection("users").document(str(ID)).update({'a': True})
                elif birthdayfinal != current_time and a == True:
                    dab.collection("users").document(str(ID)).update({'a': False})
                    logging.info(f'Set {ID} a to False')
            except Exception as e:
                logging.error(e)
            count = count + 1
        logging.info("Birthdays Ended\n----------")

def setup(bot):
    bot.add_cog(birthday_check(bot))
