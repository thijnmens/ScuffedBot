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
            if "810492978816090173" in str(member.roles):
                continue
            await member.edit(mute=True, deafen=True)
            logging.info(f"{x.name} muted")
        await ctx.message.delete()
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
            await ctx.guild.get_member(x.id).edit(mute=False, deafen=False)
            logging.info(f"{x.name} unmuted")
        await ctx.message.delete()
        logging.info("Finished unmuting\n-------------")
    
    @coordinator.command(aliases=["mo"])
    @commands.has_role(775663293695524905)
    async def move(self, ctx):
        logging.info("coord move ran")
        if ctx.author.voice is None:
            return await ctx.send("You aren't ini a voice channel!")
        voice = self.client.get_channel(ctx.author.voice.channel.id)
        logging.info(f"Moving players in {voice.name}")
        for x in voice.members:
            if x.id == ctx.author.id:
                continue
            member = ctx.guild.get_member(x.id)
            if "810492978816090173" in str(member.roles):
                continue
            await member.move_to(self.client.get_channel(764546987441258506))
            logging.info(f"{x.name} moved")
        await ctx.message.delete()
        logging.info("Finished moving\n-------------")

def setup(client):
    client.add_cog(coord(client))