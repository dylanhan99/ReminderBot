import datetime
import firebase_app as myFirebase

class GlobalCache:
    task = "Task"
    location = "Location"
    date = "Date"
    time = "Time"

    reminderDic = myFirebase.GetReminders()
    reminderList = reminderDic.each()

    def UpdateReminderDic():
        global reminderDic, reminderList
        reminderDic = myFirebase.GetReminders()
        reminderList = reminderDic.each()

    def ListAll(header):
        s = ""
        if header != "":
            s = "{}\n".format(header)
        i = 1
        if reminderDic.val() != None:
            for r in reminderList:
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