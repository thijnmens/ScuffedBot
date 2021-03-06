import discord
import logging
from discord.ext import commands



class text(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener('on_message')
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

    # ping
    @commands.command(case_insensitive=True)
    async def ping(self, ctx):
        logging.info('Recieved ping')
        await ctx.send(f'uwu *notices your ping* <w< ``{round(self.bot.latency * 1000)}ms``')
        logging.info(f'Response: {round(self.bot.latency * 1000)}ms\n----------')
    
    @commands.command(case_insensitive=True, aliases=["no"])  # Keep this out of the help embed ;)
    @commands.cooldown(1, 600, commands.BucketType.guild)
    async def nope(self, ctx):
        logging.info("Recieved >nope")
        await ctx.send("Join the NOPE clan <:GunChamp:796047943966523432>\nhttps://discord.gg/xH7AGnGXkf")
        logging.info("Response: Certainly not a link to the NOPE discord----------")

    @commands.command(case_insensitive=True)
    async def links(self, ctx):
        logging.info('Recieved links')
        embed = discord.Embed(
            title="Important Scuffed Links",
            description="[Discord](https://discord.gg/4bF8JAGeB3) | [Twitch](https://www.twitch.tv/scuffedtourneys) | [Challonge](https://challonge.com/users/scuffedtourney/tournaments) | [Scuffed Bot Repo](https://github.com/thijnmens/ScuffedBot)\n[BeatKhana!](https://beatkhana.com/) (since we're there sometimes)",
            color=0xff0000)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/796012513917272085/804784985961005073/hmm_yes_transparency.png")
        await ctx.send(embed=embed)
        logging.info(f'Response: embed----------')


def setup(bot):
    bot.add_cog(text(bot))
