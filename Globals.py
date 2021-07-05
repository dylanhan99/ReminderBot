import datetime
import discord.utils
import firebase_app as myFirebase
from datetime import datetime

class GlobalCache:
    task = "Task"
    location = "Location"
    date = "Date"
    time = "Time"

    rbChannelName = "bot-test"

    reminderDic = myFirebase.GetReminders()
    reminderList = reminderDic.each()

    def UpdateReminderDic():
        GlobalCache.reminderDic = myFirebase.GetReminders()
        GlobalCache.reminderList = GlobalCache.reminderDic.each()

    def DicIsEmpty():
        if GlobalCache.reminderDic.val() == None:
            return True
        return False

    def ListAll(header):
        s = ""
        if header != "":
            s = "{}\n".format(header)
        i = 1
        if GlobalCache.DicIsEmpty() == False:
            for r in GlobalCache.reminderList:
                s += GlobalCache.ListReminderFormat(i, r)
                i += 1
        else:
            s = "No reminders available."
            print("Empty list")
        return s

    def ListReminderFormat(i, r):
        s = "{0}.\t{1} @ {2}\t{3}\t{4}hrs\n".format(i, r.key(), r.val()[GlobalCache.location], r.val()[GlobalCache.date], r.val()[GlobalCache.time])
        return s

    def StringToDate(s):
        ddmmyyyy = s.split("/") # [dd, mm, yyyy]
        return datetime.date(int(ddmmyyyy[2]), int(ddmmyyyy[1]), int(ddmmyyyy[0]))

    def DateFormat(d):
        format = "%d/%m/%Y"
        try:
            datetime.strptime(d, format)
            return True
        except:
            return False

    def TimeFormat(t):
        format = "%H%M"
        try:
            datetime.strptime(t, format)
            return True
        except:
            return False

    def ToUTC(d, t):
        return