import asyncio
import discord
from discord import guild
from discord.ext import commands, tasks
import os
import schedule
import time

import firebase_app as myFirebase
import Globals
from Globals import GlobalCache

#client = discord.Client()
client = commands.Bot(command_prefix='.')
token = os.getenv("DISCORD_BOT_TOKEN")


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
		data = {GlobalCache.location: l, GlobalCache.date: d, GlobalCache.time: tm}
		if myFirebase.Add(t, data):
			GlobalCache.UpdateReminderDic()
			await ctx.send(GlobalCache.ListAll("'{}' added!".format(t)))
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
	await ctx.send(GlobalCache.ListAll(""))

@client.command()
async def Edit(ctx, *args):
	if len(args) == 0:
		await ctx.send(GlobalCache.ListAll("Select index to edit:"))
	elif len(args) == 3:
		try:
			i = int(args[0]) - 1
			t = GlobalCache.reminderList[i].key()
			k = args[1]
			v = args[2]
			if myFirebase.DoesReminderExist(t) and myFirebase.DoesKeyExist(t, k):
				if k == GlobalCache.task: # If editing task name
					data = myFirebase.GetReminder(t)
					if myFirebase.Add(v, data) and myFirebase.Remove(t):
						GlobalCache.UpdateReminderDic()
						await ctx.send(GlobalCache.ListAll("'{}' edited!".format(t)))
						print("Edited {0} to {1}".format(t, v))
					else:
						await ctx.send("Internal Error Occured.")
						err = "Firebase ADD/REMOVE function failed"
						print("Edit Failed: {}".format(err))
				else:		# If editing anything else
					data = {k: v}
					if myFirebase.Edit(t, data):
						GlobalCache.UpdateReminderDic()
						await ctx.send(GlobalCache.ListAll("'{}' edited!".format(t)))
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
		await ctx.send(GlobalCache.ListAll("Select index to remove:"))
	elif len(args) >= 1:
		try:
			i = int(args[0]) - 1
			t = GlobalCache.reminderList[i].key()
			if myFirebase.Remove(t):
				GlobalCache.UpdateReminderDic()
				await ctx.send(GlobalCache.ListAll("Removed '{}'".format(t)))
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

client.load_extension("cogs.DailyReminderCog")
client.run(token)
