from logging import info as logging_info, error as logging_error
from math import ceil
from datetime import timedelta

from discord import Embed, Colour

from discord.ext import commands


class error_handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        logging_info(f"on_command_error triggered")
        if isinstance(error, commands.BadArgument):
            logging_info("BadArgument handler ran\n----------")
            return await ctx.send("B-Baka!! You've given a bad argument!!")

        elif isinstance(error, commands.CommandNotFound):
            logging_info("CommandNotFound handler ran\n----------")
            return await ctx.send("S-Sorry Senpai, I couldn't find that command qwq", delete_after=20)

        elif isinstance(error, commands.BotMissingPermissions):
            logging_info(f"BotMissingPermissions handler ran - {error.missing_perms[0]}\n----------")
            return await ctx.send(f"Bot missing the following permissions: {error.missing_perms[0]}")

        elif isinstance(error, commands.NotOwner):
            logging_info("NotOwner handler ran\n----------")
            return await ctx.send('Only my owner can do that with me~ >w<')

        elif isinstance(error, commands.CommandOnCooldown):
            logging_info("CommandOnCooldown handler ran\n----------")
            date = str(timedelta(seconds=ceil(error.retry_after))).split(':')
            return await ctx.send(f"S-Senpai, I'm cooling down! O//w//O\nplease wait {date[0]} hours, {date[1]} minutes and {date[2]} seconds uwu")

        elif isinstance(error, commands.MissingRequiredArgument):
            logging_info("MissingRequiredArgument handler ran\n----------")
            # \n``Missing: {error.param.name}``")
            return await ctx.send(f"You didn't give a required argument, B-Baka!")

        elif isinstance(error, commands.MissingPermissions):
            logging_info("MissingPermissions handler ran\n----------")
            return await ctx.send("Sorry Senpai, you don't have the permissions for this command qwq")

        elif isinstance(error, commands.NSFWChannelRequired):
            logging_info("NSFWChannelRequired hander ran\n----------")
            return await ctx.reply("P-Pervert! <a:LoliTriggered:754632379397570620>\n``This command can only be ran in an nsfw channel``")
        
        logging_error(error)
        await ctx.send(embed=Embed(
            title="Uh oh. Something bad happened <a:ppMeltdown:754632378386874459>",
            description=f"An unhandled error occured.\nIf this keeps occuring open an [issue report](https://github.com/thijnmens/ScuffedBot/issues) or go pester one of the retards that 'code' this mess.\n\n```{error}```",
            colour=Colour.red()
        ))
        return await self.bot.get_channel(860609168741498920).send(embed=Embed(
            title=f"{ctx.command} in {ctx.guild.name}",
            description=f"{ctx.guild.id}\n**Message Content**```{ctx.message.content}```\n**Error**```{error}```",
            colour=Colour.red()
        ))


def setup(bot):
    bot.add_cog(error_handler(bot))
