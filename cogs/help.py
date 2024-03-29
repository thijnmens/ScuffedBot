from discord import Embed

from discord.ext import commands


class helpClient(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.group(invoke_without_command=True, aliases=["he"])
    async def help(self, ctx):
        embed = Embed(
            title="Help",
            description="``<text> is a mandatory argument while [text] is an optional argument``",
            color=0xff0000
        )
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/790189114711605260/c6e486bab141b997eeceb42ac5c9a3c2.png?size=256")
        embed.add_field(
            name="Sub help commands",
            value="**>help user** | command and subcommands for >user \n**>help update** | valid fields for >user update\n**>help scoresaber** | command and subcommands for >help scoresaber\n**>help neko** | command and subcommands for neko <a:HyperNeko:754632378038747177>",
            inline=False
        )
        embed.add_field(
            name=">challonge",
            value="Posts an embed of previous scuffed tournaments.",
            inline=False
        )
        embed.add_field(
            name=">links",
            value="Posts important links for Scuffed Tourneys!",
            inline=False
        )
        embed.add_field(
            name=">ping", 
            value="Pings Scuffed Bot", 
            inline=False
        )
        embed.add_field(
            name=">nhentai [id]",
            value="Posts a random doujin or fetches a certain doujin if an ID is provided. Only works in NSFW channels",
            inline=False
        )
        await ctx.send(embed=embed)

    @help.command(aliases=["u"])
    async def user(self, ctx):
        embed = Embed(
            title="Help User",
            description="These are the valid arguments for >user",
            color=0xff0000)
        embed.add_field(
            name=">user [mention]",
            value="get the info of a user",
            inline=False
        )
        embed.add_field(
            name=">user add <ScoreSaber link>",
            value="add yourself to the userbase.",
            inline=False
        )
        embed.add_field(
            name=">user update <field>",
            value="Update your info, use ``>help update`` for the fields and more info!",
            inline=False
        )
        embed.add_field(
            name=">user remove",
            value="Removes you from the database",
            inline=False
        )
        await ctx.send(embed=embed)
    
    @help.command(aliases=["up"])
    async def update(self, ctx):
        embed = Embed(
            title="Help User Update",
            description="These are the valid fields for >user update <field> <kwarg>\nAny of these can be removed with ``user remove <field>``",
            color=0xff0000
        )
        embed.add_field(
            name="username <kwarg>",
            value="Updates your username.\nYou can put anything here, so go nuts",
            inline=False
        )
        embed.add_field(
            name="scoresaber/steam/twitch/youtube/twitter/reddit <kwarg>",
            value="Updates one of your links.\nUse a valid scoresaber link, otherwise the scoresaber command won't work!\nYou can go nuts with the other links though >w<",
            inline=False
        )
        message = ""
        for x in self.bot.valid_HMD:
            message = message + x + ", "
        embed.add_field(
            name="HMD <kwarg>",
            value=f"Updates your Head Mounted Display.\nValid arguments are: ``{message[:-2]}``",
            inline=False
        )
        embed.add_field(
            name="birthday <kwarg>",
            value="Updates your birthday.\nOnly the format of ``DD/MM`` or ``DD/MM/YYYY`` will be accepted",
            inline=False
        )
        embed.add_field(
            name="status <kwarg>",
            value="Updates your status.\nYou can put anything here, so go nuts",
            inline=False
        )
        embed.add_field(
            name="pfp <kwarg>",
            value="Updates your profile picture.\nMake sure this argument is a link going to an image!\nLil' secret: You can post a saved image to discord and use the link which discord generates.",
            inline=False
        )
        embed.add_field(
            name="colour <kwarg>",
            value="Updates your profile's embed colour\nMake sure to use a hex code. You can use a site [like this](https://www.color-hex.com/) to find the colour you want!",
            inline=False
        )
        await ctx.send(embed=embed)

    @help.command(aliases=["ss"])
    async def scoresaber(self, ctx):
        embed = Embed(
            title="Help ScoreSaber",
            description="These are the valid arguments for >ScoreSaber\n~~certainly not a bad ripoff of bs bot~~",
            color=0xff0000
        )
        embed.add_field(
            name=">scoresaber [mention]",
            value="gets a user's ScoreSaber data,",
            inline=False
        )
        embed.add_field(
            name=">scoresaber topsong [song number] [mention]",
            value="gets a user's top song from ScoreSaber. **Song number has to be given if mention is given**",
            inline=False
        )
        embed.add_field(
            name=">scoresaber recentsong [song number] [mention]",
            value="gets a user's most recent song from ScoreSaber. **Song number has to be given if mention is given**",
            inline=False
        )
        embed.add_field(
            name=">scoresaber topsongs [page] [mention]",
            value="gets a user's page of top songs from ScoreSaber. **Page has to be given if mention is given**",
            inline=False
        )
        embed.add_field(
            name=">scoresaber recentsongs [page] [mention]",
            value="gets a user's page of recent songs from ScoreSaber. **Page has to be given if mention is given**",
            inline=False
        )
        embed.add_field(
            name=">scoresaber compare <first user> [second user]",
            value="Compare two users together. excluse the second user argument if you only want to compare yourself against someone else.",
            inline=False
        )
        await ctx.send(embed=embed)

    @help.command()
    async def neko(self, ctx):
        embed = Embed(
            title="Help Neko",
            description="These are the valid arguments for >neko",
            colour=0xff0000
        )
        embed.set_thumbnail(url="https://i.imgur.com/7Whb3qK.png")
        embed.add_field(
            name=">neko",
            value="Posts an image of a neko",
            inline=False
        )
        embed.add_field(
            name=">neko gif",
            value="Posts a gif of a neko",
            inline=False
        )
        embed.add_field(
            name=">neko lewd",
            value="Posts a lewd image of a neko. Only works in an NSFW channel",
            inline=False
        )
        embed.add_field(
            name=">neko lewd gif",
            value="Posts a lewd gif of a neko. Only works in an NSFW channel",
            inline=False
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(helpClient(bot))
