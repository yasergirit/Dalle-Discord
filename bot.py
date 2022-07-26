# configuration
# import config

# discord
import discord
from requests import post

# regex
import re

# base64
import io
from base64 import b64decode

import os

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('!generate:'):
        await message.channel.send("Making the request - it may take a while")
        req = post(url = "https://bf.dallemini.ai/generate", json = {'prompt': message.content.split("!generate:")[1].strip()})
        await message.channel.send("Result is completed")
        
        images = re.search('\[(.*)\]', req.content.decode("utf-8") ).group(0)
        encodings = [e.replace("\\n", "") for e in re.findall('"([^"]*)"', images)]
        myfiles = []
        for i, encoded in enumerate(encodings):
            with open("img/image{}.png".format(i), "wb") as fh:
                fh.write(b64decode(encoded))
            myfiles.append(discord.File("img/image{}.png".format(i)))
        
        await message.channel.send(files = myfiles)
        
        

client.run(os.environ.get('TOKEN'))
