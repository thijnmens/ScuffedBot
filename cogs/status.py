from logging import info as logging_info
from random import choice, getrandbits

from discord import Game, Activity, ActivityType

from discord.ext import commands, tasks


play_status_list = [
    "Aso kinda cute 😳",
    "vewy hawd!! uwu",
    "the PP grind",
    "ur mum",
    "ur mom",
    "Scuffed Saber",
    "Scuffed Walls",
    "01101000 01101001",
    "My sister is a dumbass",
    "Shiny Happy Days",
    "NEKOPARA Vol. 0",
    "NEKOPARA Vol. 1",
    "NEKOPARA Vol. 2",
    "NEKOPARA Vol. 3",
    "NEKOPARA Vol. 4"
]

watch_status_list = [
    "hentai",
    "Nekopara",
    "Taichi return?",
    "thijn cum multiple times during every turney",
    "notmyname stream hentai",
    "Aso be cute 😳",
    "You."
]


class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(hours=1)
    async def status(self):
        await self.bot.wait_until_ready()
        if getrandbits(1) == 1:
            value = choice(play_status_list)
            await self.bot.change_presence(activity=Game(name=value))
            logging_info(f"Status set to: {value}")
        else:
            value = choice(watch_status_list)
            await self.bot.change_presence(activity=Activity(name=value, type=ActivityType.watching))
            logging_info(f"Status set to: {value}")

    @commands.Cog.listener()
    async def on_ready(self):
        self.status.start()


def setup(bot):
    bot.add_cog(Status(bot))