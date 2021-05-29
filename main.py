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

def fList(header):
	s = ""
	if header != "":
		s = "{}\n".format(header)
	i = 1
	reminders = myFirebase.GetReminders()
	if reminders != False:
		for r in reminders.each():
			s += "{0}.\t{1} @ {2}\t{3}\t{4}hrs\n".format(i, r.key(), r.val()[loc], r.val()[date], r.val()[time])
			i += 1
	else:
		s = "Unknown Error Occured."
		print("List failed")
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
			await ctx.send(fList("'{}' added!".format(t)))
			print("Added {0}: {1}".format(t, data))
		else:
			await ctx.send("Unknown Error Occured.")
			print("Add Failed")
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
		await ctx.send(fList("Which reminder to edit?"))
	elif len(args) == 3:
		t = args[0]
		l = args[1]
		v = args[2]
		if l == ta: # If editing task name
			data = myFirebase.GetReminder(t).val()
			if myFirebase.Add(v, data) and myFirebase.Remove(t):
				await ctx.send(fList("'{}' edited!".format(t)))
				print("Edited {0} to {1}".format(t, v))
			else:
				await ctx.send("Unknown Error Occured.")
				print("Edit Failed")
		else:		# If editing anything else
			data = {l: v}
			if myFirebase.Edit(t, data):
				await ctx.send(fList("'{}' edited!".format(t)))
				print("Edited {0}: {1}".format(t, data))
			else:
				await ctx.send("Unknown Error Occured.")
				print("Edit Failed")
	else:
		s = "Missing parameters!\nReminder not edited."
		await ctx.send(s)
		print(s)


@client.command()
async def Remove(ctx, *args):
	if len(args) == 0:
		await ctx.send(fList("Which reminder to remove?"))
	elif len(args) >= 1:
		if myFirebase.Remove(args[0]):
			await ctx.send(fList("'{}' removed!".format(args[0])))
		else:
			await ctx.send("Unknown Error Occured.")
			print("Removal Failed")

#@client.event
#async def on_message(message):
#    if message.author == client.user:
#        return

    #if message.content.startswith('$hello'):
    #    await message.channel.send('Hello!')

client.run(token)
