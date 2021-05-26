import discord
from discord.ext import commands
import os
import json

import firebase_app as myFirebase

#client = discord.Client()
client = commands.Bot(command_prefix='.')
token = os.getenv("DISCORD_BOT_TOKEN")
loc = "Location"
date = "Date"
time = "Time"

def fList(header):
	s = ""
	if header != "":
		s = "{}\n".format(header)
	i = 1
	reminders = myFirebase.GetReminders()
	for r in reminders.each():
		s += "{0}.\t{1} @ {2}\t{3}\t{4}hrs\n".format(i, r.key(), r.val()[loc], r.val()[date], r.val()[time])
		i += 1
	return s

@client.event
async def on_ready():
    print('{0.user} is up and ready!'.format(client))

@client.command()
async def latency(ctx):
	await ctx.send('{}ms'.format(round(client.latency * 1000)))
	
@client.command()
async def Add(ctx, task, location, tdate, ttime):
	data = {loc: location, date: tdate, time: ttime}
	myFirebase.Add(task, data)
	await ctx.send(fList("'{}' added!".format(task)))

@client.command()
async def List(ctx):
	await ctx.send(fList(""))

@client.command()
async def Edit(ctx, *args):
	if len(args) == 0:
		await ctx.send(fList("Which reminder to edit?"))
	elif len(args) == 3:
		data = {args[1]: args[2]}
		myFirebase.Edit(args[0], data)
		await ctx.send(fList("'{}' edited!".format(args[0])))

@client.command()
async def Remove(ctx, *args):
	if len(args) == 0:
		await ctx.send(fList("Which reminder to remove?"))
	elif len(args) == 1:
		myFirebase.Remove(args[0])
		await ctx.send(fList("'{}' removed!".format(args[0])))

#@client.event
#async def on_message(message):
#    if message.author == client.user:
#        return

    #if message.content.startswith('$hello'):
    #    await message.channel.send('Hello!')

#client.run(token)
client.run('ODQ0Nzg5MDIwNDk1MTgzOTQ0.YKXhFQ.WBAU5pdOxKPYgemCWFpsgmiE9hM')