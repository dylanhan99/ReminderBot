import discord.utils
import datetime, dateutil
from discord.ext import commands, tasks
from datetime import datetime
from dateutil import tz

import firebase_app as myFirebase
import Globals
from Globals import GlobalCache

class DailyReminderCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.TimeCheck.start()

    def cog_unload(self):
        self.TimeCheck.cancel()

    def PrepareRemindersToPrint(self, GMTp8):
        overdue = "OVERDUE\n"
        today = "TODAY\n"
        others = "OTHERS\n"
        i = 1
        j = 1
        k = 1
        for r in myFirebase.GetReminders().each():
            rDate = GlobalCache.StringToDate(r.val()[GlobalCache.date])
            if rDate < GMTp8.date():
                overdue += GlobalCache.ListReminderFormat(i, r)
                i += 1
            elif rDate == GMTp8.date():
                today += GlobalCache.ListReminderFormat(j, r)
                j += 1
            else:
                others += GlobalCache.ListReminderFormat(k, r)
                k += 1
        d  = "================================\n"
        s  = d
        s += "========   DAILY REMINDERS:   ========\n"
        s += d
        s += "{0}\n{1}\n{2}".format(overdue, today, others)
        s += d
        return s

    @tasks.loop(minutes=1.0)
    async def TimeCheck(self):
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        utc = datetime.utcnow().replace(tzinfo=from_zone)
        GMTp8 = utc.astimezone(to_zone)

        if GMTp8.hour == 0 and GMTp8.minute == 0:
            channel = discord.utils.get(self.bot.get_all_channels(), name='bot-test')
            await channel.send(self.PrepareRemindersToPrint(GMTp8))
            
    @TimeCheck.before_loop
    async def before_TimeCheck(self):
        print('DailyReminderCog waiting...')
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(DailyReminderCog(bot))