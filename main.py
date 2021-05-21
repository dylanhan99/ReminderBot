import discord
import os

client = discord.Client()

#BOT_TOKEN = environ['TOKEN']
token = os.getenv("DISCORD_BOT_TOKEN")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(token)