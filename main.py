import discord

settings = {}
with open('config.txt', 'r') as f:
    for i in f:
        line = i.split('=')
        settings[line[0]] = line[1]
        print(settings)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

if __name__ == '__main__':
    client.run(settings['TOKEN'])
    x = client.user
    print(x)
