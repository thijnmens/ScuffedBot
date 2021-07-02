# I can assure you, this cog is vital for the performance and useability of Scuffed Bot
#https://www.nekos.life/api/v2/endpoints

from io import BytesIO
from aiohttp import ClientSession
from json import loads
from logging import info as logging_info

from discord import File

from discord.ext import commands

async def image(self, link):
    async with ClientSession() as session:
        async with session.get(link) as resp:
            json_data = loads(await resp.text())
            logging_info(json_data["url"])
            async with session.get(json_data["url"]) as resp:
                return BytesIO(await resp.read())


class Neko(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.group(invoke_without_command=True, )
    async def neko(self, ctx):
        async with ctx.channel.typing():
            await ctx.reply(file=File(await image(self, "https://nekos.life/api/v2/img/neko"), "neko.png"))
        
    @neko.command()
    async def gif(self, ctx):
        async with ctx.channel.typing():
            await ctx.reply(file=File(await image(self, "https://nekos.life/api/v2/img/ngif"), "neko.gif"))

    @neko.group(invoke_without_command=True, )
    @commands.is_nsfw()
    async def lewd(self, ctx):
        async with ctx.channel.typing():
            await ctx.reply(file=File(await image(self, "https://nekos.life/api/v2/img/lewd"), "neko.png"))

    @lewd.command(aliases=["gif"])
    @commands.is_nsfw()
    async def lewd_gif(self, ctx):
        async with ctx.channel.typing():
            await ctx.reply(file=File(await image(self, "https://nekos.life/api/v2/img/nsfw_neko_gif"), "neko.gif"))


def setup(bot):
    bot.add_cog(Neko(bot))
