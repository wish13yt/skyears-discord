
import discord
import os
from pathlib import Path
import shutil
import http.client
import json
class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.content.startswith('!link'):
            msgcontent = message.content
            print("message content: " + msgcontent)
            did = msgcontent[6:]
            print("truncated did: " + did)
            print("creating file!")
            txt = Path("db/" + str(message.author.id) + ".txt")
            if txt.is_file():
                await message.reply("I've already linked you! Run !unlink to unlink.")
            else:
                with open("db/" + str(message.author.id) + ".txt", 'x+') as file:
                    print("file made! writing...")
                    file.write(did)
                    print("wrote!")
                    await message.reply("Created file in db/" + str(message.author.id) + ".txt")
        if message.content.startswith('!erasedb'):
            if message.author.id == 1409704302238502935:
                await message.reply("The database was deleted.")
                shutil.rmtree("db")
                os.makedirs("db")
            else:
                return
        if message.content.startswith('!fm'):
            with open('db/' + str(message.author.id) + ".txt") as f: didfile = f.read()
            conn = http.client.HTTPSConnection("api.rocksky.app")
            payload = ''
            headers = {}
            conn.request("GET", "/xrpc/app.rocksky.actor.getActorScrobbles?limit=1&offset=0&did=" + didfile, payload, headers)
            res = conn.getresponse()
            data = res.read()
            print(data.decode("utf-8"))
            parsed = json.loads(data.decode("utf-8"))
            scrobbles = parsed.get("scrobbles", [])
            if scrobbles:
                latest = scrobbles[0]
                embedVar = discord.Embed(title=latest['title'], color=0xff0177)
                embedVar.add_field(name="", value=latest['artist'], inline=False)
                embedVar.set_thumbnail(url=latest['albumArt'])
                user = await self.fetch_user(message.author.id)
                embedVar.set_footer(text="Requested by " + user.global_name + " (" + user.name + ") | Via rocksky.app")
                await message.reply(embed=embedVar)
        if message.content.startswith('!whatsmydid'):
            with open('db/' + str(message.author.id) + ".txt") as f: didfile = f.read()
            await message.reply("The DID linked to your account is: " + didfile)
        if message.content.startswith("!unlink"):
            if os.path.exists("db/" + str(message.author.id) + ".txt"):
                os.remove("db/" + str(message.author.id) + ".txt")
                await message.reply("Your DID file has been deleted! To relink, run !link with your DID.")
            else:
                await message.reply("DID file not found, and was not deleted.")
        if message.content.startswith("!skyhelp"):
            await message.reply("SkyEars Help\n !link [did]: Link your ATProto DID to use the bot! \n !unlink: Unlink your DID! \n !art: Shows the latest song's cover art. \n !fm: See your latest Rocksky song! \n !whatsmydid: See your DID you have linked!\n Licensed under GPL-3.0 by Freakybob Team. Not associated with Rocksky or associates.")
        if message.content.startswith("!art"):
            with open('db/' + str(message.author.id) + ".txt") as f: didfile = f.read()
            conn = http.client.HTTPSConnection("api.rocksky.app")
            payload = ''
            headers = {}
            conn.request("GET", "/xrpc/app.rocksky.actor.getActorScrobbles?limit=1&offset=0&did=" + didfile, payload, headers)
            res = conn.getresponse()
            data = res.read()
            print(data.decode("utf-8"))
            parsed = json.loads(data.decode("utf-8"))
            scrobbles = parsed.get("scrobbles", [])
            if scrobbles:
                latest = scrobbles[0]
                await message.reply(latest['albumArt'])
        if message.content.startswith("!cat"):
            await message.reply("https://cataas.com/cat")
        if message.content.startswith("!countday"):
            with open('db/' + str(message.author.id) + ".txt") as f: didfile = f.read()
            conn = http.client.HTTPSConnection("api.rocksky.app")
            payload = ''
            headers = {}
            conn.request("GET", "/xrpc/app.rocksky.charts.getScrobblesChart?did=" + didfile, payload, headers)
            res = conn.getresponse()
            data = res.read()
            print(data.decode("utf-8"))
            parsed = json.loads(data.decode("utf-8"))
            scrobbles = parsed.get("scrobbles", [])
            if scrobbles:
                latest = scrobbles[-1]
                await message.reply("Today's scrobble count for you: " + str(latest['count']) + " (uses UTC time)")
intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run('your discord bot token here')