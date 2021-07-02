from discord import Embed

from discord.ext import commands



class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener('on_message')
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

    # ping
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'uwu *notices your ping* <w< ``{round(self.bot.latency * 1000)}ms``')
    
    @commands.command(aliases=["no"])  # Keep this out of the help embed ;)
    @commands.cooldown(1, 600, commands.BucketType.guild)
    async def nope(self, ctx):
        await ctx.send("Join the NOPE clan <:GunChamp:796047943966523432>\nhttps://discord.gg/xH7AGnGXkf")

    @commands.command(aliases=["dg","disability_gang"]) 
    @commands.cooldown(1, 600, commands.BucketType.guild)
    async def disability(self, ctx):
        await ctx.send("Join the Disability Gang <:AYAYA:754632377715654677>\nhttps://discord.gg/XxKkQdRpCD") #thijn post the videos else the ayaya gets it

    @commands.command()
    async def links(self, ctx):
        embed = Embed(
            title="Important Scuffed Links",
            description="[Discord](https://discord.gg/4bF8JAGeB3) | [Twitch](https://www.twitch.tv/scuffedtourneys) | [Challonge](https://challonge.com/users/scuffedtourney/tournaments) | [Scuffed Bot Repo](https://github.com/thijnmens/ScuffedBot)\n[BeatKhana!](https://beatkhana.com/) (since we're there sometimes)",
            color=0xff0000)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/796012513917272085/804784985961005073/hmm_yes_transparency.png")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(General(bot))
