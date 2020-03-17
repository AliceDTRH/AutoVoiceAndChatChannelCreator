import dataset
import discord
import datetime
import random
import subprocess as sp
import asyncio
from discord.ext import commands, tasks


class Util_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.deleteTime = 5# * 60 
        self.joinChannel = 679479605303967767
        self.catID = 688010755643015180
        self.guildID = 679479587155083309
        self.pchannels = {}
        self.db = dataset.connect('sqlite:///MyData.db')['pchannels']
        self.loaded = False

    async def getCategoryFromID(self, guild: discord.Guild, ID: int):
        for cat in guild.categories:
            if cat.id == ID:
                return cat

    async def ccreate (self, member: discord.Member, channelname: str):
        guild = member.guild

        if hasattr(self, 'voiceCat') == False:
            self.voiceCat = await self.getCategoryFromID(guild, self.catID)

        tc = await guild.create_text_channel(channelname, category=self.voiceCat)
        vc = await guild.create_voice_channel(channelname, category=self.voiceCat)

        self.pchannels[member.id] = [tc, vc, datetime.datetime.now()]
        self.db.insert(dict(id=member.id, tc=tc.id, vc=vc.id, created=datetime.datetime.now()))
        await member.move_to(self.pchannels[member.id][1])


    async def on_voice_state_update(self, member, before, after):
        if self.loaded == False:
            await self.load()
            self.loaded = True

        if before.channel == None and after.channel.id == self.joinChannel:
            if member.id not in self.pchannels:
                print("Calling ccreate")
                await self.ccreate(member, member.display_name+"s-chat")
            else:
                print("Moving "+str(member.id)+" to "+str(self.pchannels[member.id][1]))
                await member.move_to(self.pchannels[member.id][1])
        if member.id in self.pchannels:
            if before.channel == self.pchannels[member.id][1] and after.channel != self.pchannels[member.id][1]:
                await self.QueueDelete(member.id)

    async def QueueDelete(self, memberid: int):
        bot = self.bot
        while bot.get_user(memberid) not in self.pchannels[memberid][1].members:
            if len(self.pchannels[memberid][1].members) == 0:
                await asyncio.sleep(self.deleteTime)
                if len(self.pchannels[memberid][1].members) == 0:
                    await self.pchannels[memberid][0].delete()
                    await self.pchannels[memberid][1].delete()
                    del self.pchannels[memberid]
                    self.db.delete(id=memberid)
                    break
            else:
                await asyncio.sleep(self.deleteTime/2)

    async def load(self):
        for e in self.db:
            self.pchannels[e['id']] = [self.bot.get_channel(int(e['tc'])), self.bot.get_channel(int(e['vc'])), e['created']]

    @commands.has_guild_permissions(administrator=True)
    @commands.command()
    async def reset(self, ctx):
        self.db.delete()
        self.pchannels = {}

        guild = self.bot.get_guild(self.guildID)
        cat = await self.getCategoryFromID(guild, self.catID)
        for channel in cat.channels:
            await channel.delete(reason="Reset command used!")




    async def close(self):
        print("close()")

def setup(bot):
    bot.add_cog(Util_Commands(bot))
