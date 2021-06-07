import discord.utils
from discord.ext import commands, tasks
import datetime, dateutil
from datetime import datetime
from dateutil import tz

import firebase_app as myFirebase
import Globals
from Globals import GlobalCache

class DailyReminderCog(commands.Cog):
    def __init__(self, bot):
        self.index = 0
        self.bot = bot
        self.TimeCheck.start()

    def cog_unload(self):
        self.TimeCheck.cancel()

    def printReminders():
        return ""

    @tasks.loop(minutes=1.0)
    async def TimeCheck(self):
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        utc = datetime.utcnow().replace(tzinfo=from_zone)
        GMTp8 = utc.astimezone(to_zone)

        overdue = "OVERDUE\n"
        today = "TODAY\n"
        others = "OTHERS\n"
        if GMTp8.hour == 0 and GMTp8.minute == 0:
            i = 1
            j = 1
            k = 1
            for r in myFirebase.GetReminders().each():
                rDate = GlobalCache.StringToDate(r.val()[GlobalCache.date])
                rVal = r.val()
                if rDate < GMTp8.date():
                    overdue += "{0}.\t{1} @ {2}\t{3}\t{4}hrs\n".format(i, r.key(), rVal[GlobalCache.location], rVal[GlobalCache.date], rVal[GlobalCache.time])
                    i += 1
                elif rDate == GMTp8.date():
                    today += "{0}.\t{1} @ {2}\t{3}\t{4}hrs\n".format(j, r.key(), rVal[GlobalCache.location], rVal[GlobalCache.date], rVal[GlobalCache.time])
                    j += 1
                else:
                    others += "{0}.\t{1} @ {2}\t{3}\t{4}hrs\n".format(k, r.key(), rVal[GlobalCache.location], rVal[GlobalCache.date], rVal[GlobalCache.time])
                    k += 1
            s = "{0}\n{1}\n{2}".format(overdue, today, others)
            channel = discord.utils.get(self.bot.get_all_channels(), name='bot-test')
            await channel.send(s)
            
    @TimeCheck.before_loop
    async def before_TimeCheck(self):
        print('DailyReminderCog waiting...')
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(DailyReminderCog(bot))