import math, logging, datetime
from discord.ext import commands


class error_handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        logging.info(f"on_command_error triggered")
        if isinstance(error, commands.BadArgument):
            logging.info("BadArgument handler ran\n----------")
            return await ctx.send("B-Baka!! You've given a bad argument!!")

        elif isinstance(error, commands.CommandNotFound):
            logging.info("CommandNotFound handler ran\n----------")
            return await ctx.send("S-Sorry Senpai, I couldn't find that command qwq", delete_after=20)

        elif isinstance(error, commands.BotMissingPermissions):
            logging.info(f"BotMissingPermissions handler ran - {error.missing_perms[0]}\n----------")
            return await ctx.send(f"Bot missing the following permissions: {error.missing_perms[0]}")

        elif isinstance(error, commands.NotOwner):
            logging.info("NotOwner handler ran\n----------")
            return await ctx.send('Only my owner can do that with me~ >w<')

        elif isinstance(error, commands.CommandOnCooldown):
            logging.info("CommandOnCooldown handler ran\n----------")
            date = str(datetime.timedelta(seconds=math.ceil(error.retry_after))).split(':')
            return await ctx.send(f"S-Senpai, I'm cooling down! O//w//O\nplease wait {date[0]} hours, {date[1]} minutes and {date[2]} seconds uwu")

        elif isinstance(error, commands.MissingRequiredArgument):
            logging.info("MissingRequiredArgument handler ran\n----------")
            # \n``Missing: {error.param.name}``")
            return await ctx.send(f"You didn't give a required argument, B-Baka!")

        elif isinstance(error, commands.MissingPermissions):
            logging.info("MissingPermissions handler ran\n----------")
            return await ctx.send("Sorry Senpai, you don't have the permissions for this command qwq")

        elif isinstance(error, commands.NSFWChannelRequired):
            logging.info("NSFWChannelRequired hander ran\n----------")
            return await ctx.reply("P-Pervert! <a:LoliTriggered:754632379397570620>\n``This command can only be ran in an nsfw channel``")
        
        elif isinstance(error, commands.CheckFailure):
            logging.error(f"{error}\n----------")

        logging.error(f"{error}\n----------")


def setup(bot):
    bot.add_cog(error_handler(bot))
