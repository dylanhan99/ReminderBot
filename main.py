import discord
from discord.ext import commands
import os
import json

import firebase_app as myFirebase

#client = discord.Client()
client = commands.Bot(command_prefix='.')
token = os.getenv("DISCORD_BOT_TOKEN")

@client.event
async def on_ready():
    print('{0.user} is up and ready!'.format(client))

@client.command()
async def latency(ctx):
	await ctx.send('{}ms'.format(round(client.latency * 1000)))
	
@client.command()
async def Add(ctx, task, location, date, time):
	data = {"Location": location, "Date": date, "Time": time}
	myFirebase.Add(task, data)

@client.command()
async def List(ctx):
	s = ""
	i = 1
	reminders = myFirebase.GetReminders()
	for r in reminders.each():
		s += "{0}.\t{1} @ {2}\t{3}\t{4}hrs\n".format(i, r.key(), r.val()["Location"], r.val()["Date"], r.val()["Time"])
		i += 1
	await ctx.send(s)

#@client.event
#async def on_message(message):
#    if message.author == client.user:
#        return

    #if message.content.startswith('$hello'):
    #    await message.channel.send('Hello!')

#client.run(token)
client.run('ODQ0Nzg5MDIwNDk1MTgzOTQ0.YKXhFQ.WBAU5pdOxKPYgemCWFpsgmiE9hM')