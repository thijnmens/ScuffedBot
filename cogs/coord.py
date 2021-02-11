import discord
import logging
from discord.ext import commands


class coord(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=["coord","c"])
    @commands.has_role(775663293695524905)
    async def coordinator(self, ctx):
        await ctx.send("Hi coordinator-kun ^w^")

    @coordinator.command(aliases=["m"])
    @commands.has_role(775663293695524905)
    async def mute(self, ctx):
        logging.info("coord mute ran")
        if ctx.author.voice is None:
            return await ctx.send("You aren't in a voice channel!")
        voice = self.client.get_channel(ctx.author.voice.channel.id)
        logging.info(f"muting in {voice.name}")
        for x in voice.members:
            if x.id == ctx.author.id:
                continue
            member = ctx.guild.get_member(x.id)
            await member.edit(mute=True, deafen=True)
            logging.info(f"{x.name} muted")
        logging.info("Finished muting\n-------------")

    @coordinator.command(aliases=["um"])
    @commands.has_role(775663293695524905)
    async def unmute(self, ctx):
        logging.info("coord unmute ran")
        if ctx.author.voice is None:
            return await ctx.send("You aren't in a voice channel!")
        voice = self.client.get_channel(ctx.author.voice.channel.id)
        logging.info(f"unmuting in {voice.name}")
        for x in voice.members:
            if x.id == ctx.author.id:
                continue
            member = ctx.guild.get_member(x.id)
            await member.edit(mute=False, deafen=False)
            logging.info(f"{x.name} unmuted")
        logging.info("Finished unmuting\n-------------")
    

def setup(client):
    client.add_cog(coord(client))