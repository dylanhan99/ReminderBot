import discord
import os

client = discord.Client()

#BOT_TOKEN = environ['TOKEN']

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run('ODQ0Nzg5MDIwNDk1MTgzOTQ0.YKXhFQ.WBAU5pdOxKPYgemCWFpsgmiE9hM')