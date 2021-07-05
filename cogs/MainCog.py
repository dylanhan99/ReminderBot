import discord.utils
from discord.ext import commands, tasks

import firebase_app as myFirebase
import Globals
from Globals import GlobalCache

class MainCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.channel = discord.utils.get(self.bot.get_all_channels(), name=GlobalCache.rbChannelName)

    @commands.command()
    async def Ping(self, ctx):
        await self.channel.send('{}ms'.format(round(self.bot.latency * 1000)))

    @commands.command()
    async def Add(self, ctx, *args):
        if len(args) >= 4:
            t = args[0]
            l = args[1]
            d = args[2]
            tm = args[3]
            if (GlobalCache.DateFormat(d) and GlobalCache.TimeFormat(tm)) == False:
                await self.channel.send("Date or Time format is incorrect.\nTo be in dd/mm/yyyy and hhmm format respectively.")
                err = "User Input: Incorrect Date/Time format"
                print("Add Failed: {}".format(err))
                return
            data = {GlobalCache.location: l, GlobalCache.date: d, GlobalCache.time: tm}
            if myFirebase.Add(t, data):
                GlobalCache.UpdateReminderDic()
                await self.channel.send(GlobalCache.ListAll("'{}' added!".format(t)))
                print("Added {0}: {1}".format(t, data))
            else:
                await self.channel.send("Internal Error Occured.")
                err = "Firebase ADD function failed"
                print("Add Failed: {}".format(err))
        else:
            await self.channel.send("Missing parameters!\nReminder not added.")
            err = "User Input: Missing parameters"
            print("Add Failed: {}".format(err))

    @commands.command()
    async def List(self, ctx):
        await self.channel.send(GlobalCache.ListAll(""))

    @commands.command()
    async def Edit(self, ctx, *args):
        if len(args) == 0:
            await self.channel.send(GlobalCache.ListAll("Select index to edit:"))
        elif len(args) == 3:
            try:
                if GlobalCache.DicIsEmpty():
                    await self.channel.send("No reminders available.")
                    print("Empty list")
                    return
                i = int(args[0]) - 1
                t = GlobalCache.reminderList[i].key()
                k = args[1]
                v = args[2]
                if (myFirebase.DoesReminderExist(t) and k == GlobalCache.task) or \
                    (myFirebase.DoesReminderExist(t) and myFirebase.DoesKeyExist(t, k)):
                    if k == GlobalCache.task: # If editing task name
                        data = myFirebase.GetReminder(t)
                        if myFirebase.Add(v, data) and myFirebase.Remove(t):
                            GlobalCache.UpdateReminderDic()
                            await self.channel.send(GlobalCache.ListAll("'{}' edited!".format(t)))
                            print("Edited {0} to {1}".format(t, v))
                        else:
                            await self.channel.send("Internal Error Occured.")
                            err = "Firebase ADD/REMOVE function failed"
                            print("Edit Failed: {}".format(err))
                    else:		# If editing anything else
                        if k == GlobalCache.date and GlobalCache.DateFormat(v) == False:
                            await self.channel.send("Date format is incorrect.\nTo be in dd/mm/yyyy format.")
                            err = "User Input: Incorrect Date format"
                            print("Add Failed: {}".format(err))
                            return
                        elif k == GlobalCache.time and GlobalCache.TimeFormat(v) == False:
                            await self.channel.send("Time format is incorrect.\nTo be in hhmm format.")
                            err = "User Input: Incorrect Time format"
                            print("Add Failed: {}".format(err))
                            return
                        data = {k: v}
                        if myFirebase.Edit(t, data):
                            GlobalCache.UpdateReminderDic()
                            await self.channel.send(GlobalCache.ListAll("'{}' edited!".format(t)))
                            print("Edited {0}: {1}".format(t, data))
                        else:
                            await self.channel.send("Internal Error Occured.")
                            err = "Firebase EDIT function failed"
                            print("Edit Failed: {}".format(err))
                else:
                    await self.channel.send("Task/Key is invalid.")
                    err = "Task/Key is invalid"
                    print("Edit Failed: {}".format(err))
            except:
                await self.channel.send("Unknown Error Occured.")
                err = "Unknown error occured"
                raise ValueError("Edit Failed: {}".format(err))
        else:
            s = "Missing parameters!\nReminder not edited."
            await self.channel.send(s)
            print(s)

    @commands.command()
    async def Remove(self, ctx, *args):
        if len(args) == 0:
            await self.channel.send(GlobalCache.ListAll("Select index to remove:"))
        elif len(args) >= 1:
            try:
                if GlobalCache.DicIsEmpty():
                    await self.channel.send("No reminders available.")
                    print("Empty list")
                    return
                i = int(args[0]) - 1
                t = GlobalCache.reminderList[i].key()
                if myFirebase.Remove(t):
                    GlobalCache.UpdateReminderDic()
                    await self.channel.send(GlobalCache.ListAll("Removed '{}'".format(t)))
                    print("Removed '{}'".format(t))
                else:
                    await self.channel.send("Internal Error Occured.")
                    err = "Firebase REMOVE function failed"
                    print("Remove Failed: {}".format(err))
            except:
                await self.channel.send("Unknown Error Occured.")
                err = "Unknown error occured"
                raise ValueError("Remove Failed: {}".format(err))
        else:
            await self.channel.send("Invalid Arguments.")
            err = "Invalid arguments"
            print("Remove Failed: {}".format(err))
            
def setup(bot):
    bot.add_cog(MainCog(bot))