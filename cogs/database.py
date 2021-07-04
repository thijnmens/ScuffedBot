from logging import info as logging_info, error as logging_error

from firebase_admin import firestore

from discord.ext import commands


dab = firestore.client()

class database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def db(self, ctx, argument0=None, argument1=None, argument2=None):
        if argument0 == 'add' and argument1 == 'inv':
            ref = dab.collection('users').document('collectionlist').get().get('array')
            amount = len(ref) - 1
            count = 0
            while (count <= amount):
                try:
                    ID = ref[count]
                    inv = dab.collection('users').document(str(ID)).get().get('inv')
                    inv.append(argument2)
                    dab.collection('users').document(str(ID)).update({'inv': inv})
                except Exception as e:
                    logging_error(e)
                count = count + 1
            logging_info("updated database\n----------")
            await ctx.send('I\'ve updated the database senpai UwU')
        elif argument0 =='add':
            ref = dab.collection('users').document('collectionlist').get().get('array')
            amount = len(ref) - 1
            count = 0
            while (count <= amount):
                try:
                    ID = ref[count]
                    inv = dab.collection('users').document(str(ID)).update({f'{argument1}': argument2})
                except Exception as e:
                    logging_error(e)
                count = count + 1
            await ctx.send('I\'ve updated the database senpai UwU')

def setup(bot):
    bot.add_cog(database(bot))