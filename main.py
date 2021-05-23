import discord
from discord.ext import commands
import os
import json

import misc

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
	dic = misc.ConvertToDic(task, location, date, time)
	misc.AddToFile(dic)

@client.command()
async def List(ctx):
	s = ""
	i = 1
	reminders = misc.GetData()
	for r in reminders:
		s += "{0}.\t{1} @ {2}\t{3}\t{4}hrs\n".format(i, r, reminders[r]["Location"], reminders[r]["Date"], reminders[r]["Time"])
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