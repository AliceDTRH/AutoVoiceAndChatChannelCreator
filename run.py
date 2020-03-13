import bot_pkg
import discord

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')

client = MyClient()
client.run('Njg3ODI5MjQyMzEzOTY1NjM4.Xmrc7Q.sokWwuD1BUhiq7Xa6uPphcX2lwY')
