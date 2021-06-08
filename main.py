import asyncio
import discord
from discord import guild
from discord.ext import commands, tasks
import os
import schedule
import time

import Globals
from Globals import GlobalCache

#client = discord.Client()
client = commands.Bot(command_prefix='.')
token = os.getenv("DISCORD_BOT_TOKEN")

@client.event
async def on_ready():
    print('{0.user} is up and ready!'.format(client))

#@client.command()
#async def Ping(ctx):
#	await ctx.send('{}ms'.format(round(client.latency * 1000)))

client.load_extension("cogs.MainCog")
client.load_extension("cogs.DailyReminderCog")
client.run(token)
