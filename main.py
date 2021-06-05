import discord
from discord.ext import commands
import os
import json

import firebase_app as myFirebase

#client = discord.Client()
client = commands.Bot(command_prefix='.')
token = os.getenv("DISCORD_BOT_TOKEN")
ta = "Task"
loc = "Location"
date = "Date"
time = "Time"

reminderDic = myFirebase.GetReminders()
reminderList = reminderDic.each()

def UpdateReminderDic():
	global reminderDic
	global reminderList
	reminderDic = myFirebase.GetReminders()
	reminderList = reminderDic.each()

def iGetReminderFromDic(index):
	count = 0
	for r in reminderDic.each():
		if count == index:
			return r
	return None

def fList(header):
	s = ""
	if header != "":
		s = "{}\n".format(header)
	i = 1
	if reminderDic.val() != None:
		for r in reminderList:
			s += "{0}.\t{1} @ {2}\t{3}\t{4}hrs\n".format(i, r.key(), r.val()[loc], r.val()[date], r.val()[time])
			i += 1
	else:
		s = "No reminders available."
		print("Empty list")
	return s

@client.event
async def on_ready():
    print('{0.user} is up and ready!'.format(client))

@client.command()
async def Ping(ctx):
	await ctx.send('{}ms'.format(round(client.latency * 1000)))
	
@client.command()
async def Add(ctx, *args):
	if len(args) >= 4:
		t = args[0]
		l = args[1]
		d = args[2]
		tm = args[3]
		data = {loc: l, date: d, time: tm}
		if myFirebase.Add(t, data):
			UpdateReminderDic()
			await ctx.send(fList("'{}' added!".format(t)))
			print("Added {0}: {1}".format(t, data))
		else:
			await ctx.send("Internal Error Occured.")
			err = "Firebase ADD function failed"
			print("Add Failed: {}".format(err))
	else:
		s = "Missing parameters!\nReminder not added."
		await ctx.send(s)
		print(s)

@client.command()
async def List(ctx):
	await ctx.send(fList(""))

@client.command()
async def Edit(ctx, *args):
	if len(args) == 0:
		await ctx.send(fList("Select index to edit:"))
	elif len(args) == 3:
		try:
			i = int(args[0]) - 1
			t = reminderList[i].key()
			k = args[1]
			v = args[2]
			if myFirebase.DoesReminderExist(t) and myFirebase.DoesKeyExist(t, k):
				if k == ta: # If editing task name
					data = myFirebase.GetReminder(t)
					if myFirebase.Add(v, data) and myFirebase.Remove(t):
						UpdateReminderDic()
						await ctx.send(fList("'{}' edited!".format(t)))
						print("Edited {0} to {1}".format(t, v))
					else:
						await ctx.send("Internal Error Occured.")
						err = "Firebase ADD/REMOVE function failed"
						print("Edit Failed: {}".format(err))
				else:		# If editing anything else
					data = {k: v}
					if myFirebase.Edit(t, data):
						UpdateReminderDic()
						await ctx.send(fList("'{}' edited!".format(t)))
						print("Edited {0}: {1}".format(t, data))
					else:
						await ctx.send("Internal Error Occured.")
						err = "Firebase EDIT function failed"
						print("Edit Failed: {}".format(err))
			else:
				await ctx.send("Task/Key is invalid.")
				err = "Task/Key is invalid"
				print("Edit Failed: {}".format(err))
		except:
			await ctx.send("Unknown Error Occured.")
			err = "Unknown error occured"
			print("Edit Failed: {}".format(err))
	else:
		s = "Missing parameters!\nReminder not edited."
		await ctx.send(s)
		print(s)

@client.command()
async def Remove(ctx, *args):
	if len(args) == 0:
		await ctx.send(fList("Select index to remove:"))
	elif len(args) >= 1:
		try:
			i = int(args[0]) - 1
			t = reminderList[i].key()
			if myFirebase.Remove(t):
				UpdateReminderDic()
				await ctx.send(fList("Removed '{}'".format(t)))
				print("Removed '{}'".format(t))
			else:
				await ctx.send("Internal Error Occured.")
				err = "Firebase REMOVE function failed"
				print("Remove Failed: {}".format(err))
		except:
			await ctx.send("Unknown Error Occured.")
			err = "Unknown error occured"
			print("Remove Failed: {}".format(err))
	else:
		await ctx.send("Invalid Arguments.")
		err = "Invalid arguments"
		print("Remove Failed: {}".format(err))

#@client.event
#async def on_message(message):
#    if message.author == client.user:
#        return

    #if message.content.startswith('$hello'):
    #    await message.channel.send('Hello!')

client.run(token)
