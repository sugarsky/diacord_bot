import discord
import asyncio
import json
import re
from emoji import emojize, demojize
from pprint import pprint as pp

settings = {}
with open('config.txt', 'r') as f:
    for i in f:
        line = i.split('=')
        settings[line[0]] = line[1]
        print(settings)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def cats(mode, dict=None, path='cats.json'):
    with open(path, mode) as f:
        if mode == 'r':
            try:
                return json.load(f)
            except:
                return {}
        elif mode == 'w':
            json.dump(dict, f, ensure_ascii=True, indent=2)

async def channel_check(client, name):
    for channel in client.get_all_channels():
        if emojize(demojize(channel.name), variant='text_type') == emojize(name, variant='text_type'):
            return channel
        print(f"{emojize(demojize(channel.name), variant='text_type')} <> {emojize(name, variant='text_type')}")
    return False

async def reaction_check(client, message, expectation=False):
    def check(reaction, user):
        return user == message.author and reaction
    try:
        reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
        print(expectation)
        print(reaction.emoji)
        if expectation and expectation == reaction.emoji:
            return True
        elif expectation:
            return False
        else:
            return reaction
    except asyncio.TimeoutError:
        await message.channel.send('Waited too long for responce')
        return False

async def rename_channel(channel, new_name):
    try:
        await channel.edit(
            name=new_name,
            topic=channel.topic, 
            position=channel.position, 
            nsfw=channel.nsfw, 
            sync_permissions=channel.permissions_synced, 
            category=channel.category, 
            slowmode_delay=channel.slowmode_delay, 
            type=channel.type,
            overwrites=channel.overwrites,
            default_auto_archive_duration=channel.default_auto_archive_duration
        )
        return True
    except:
        return False


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    elif message.content.startswith('$exit'):
        await message.channel.send('Terminating connection!')
        await client.close()
    elif message.content.startswith('$new_cat'):
        cats_old = cats('r')
        cats_new = cats_old.copy()
        for old_cat, old_emoji in cats_old.items():
            if await channel_check(client=client, name=f'{old_emoji}-{old_cat}') == False:
                del(cats_new[old_cat])
        cats('w', cats_new)
        cats_old = cats('r')
        category = [i for i in message.guild.categories if i.name == 'nsfw']
        new_cat = re.sub('\$new_cat ', '', message.content)
        if new_cat == '$new_cat':
            await message.channel.send('Please write the name of category in format "$new_cat <name>"')
        else:
            await message.channel.send('Place reaction that fits new category')
            reaction = await reaction_check(client=client, message=message)
            if reaction:
                new_emoji = demojize(reaction.emoji)
                if new_cat not in cats_old.keys() and new_emoji not in cats_old.values():
                    await message.guild.create_text_channel(f'{emojize(new_emoji)} {new_cat}', category = category[0])
                    await message.channel.send(f'Channel "#{emojize(new_emoji)}-{new_cat}" was created!')
                    cats_old[new_cat] = new_emoji
                else:
                    for old_cat, old_emoji in cats_old.items():
                        if   old_cat == new_cat and old_emoji == new_emoji:
                            await message.channel.send(f'Channel "#{emojize(old_emoji)}-{old_cat}" already exists')
                        elif old_cat == new_cat and old_emoji != new_emoji:
                            await message.channel.send(f'Category "#{emojize(old_emoji)}-{old_cat}" already exists. Want change emoji for this category?')
                            if await reaction_check(client=client, message=message, expectation=emojize(':check_mark_button:')):
                                channel = await channel_check(client=client, name=f'{old_emoji}-{old_cat}')
                                if await rename_channel(channel, f'{emojize(new_emoji)}-{new_cat}'):
                                    await message.channel.send(f'Category "#{emojize(old_emoji)}-{old_cat}" was renamed to "#{emojize(new_emoji)}-{new_cat}".')
                                    cats_old[new_cat] = new_emoji
                                    cats('w', cats_old)
                                else:
                                    await message.channel.send(f'Unexpected error happened while I tried to rename this channel. May the God forgive us.')
                                    break
                            else:
                                await message.channel.send('Mission failed. Try again next time!')
                                break
                        elif old_cat != new_cat and old_emoji == new_emoji:
                            await message.channel.send(f'Category "#{emojize(old_emoji)}-{old_cat}" already exists. Want change emoji for this category?')
                            if await reaction_check(client=client, message=message, expectation=emojize(':check_mark_button:')):
                                await message.channel.send(f'Place new reaction for category {old_cat}')
                                replacement = await reaction_check(client=client, message=message)
                                if replacement:
                                    channel = await channel_check(client=client, name=f'{old_emoji}-{old_cat}')
                                    if await rename_channel(channel, f'{replacement.emoji}-{old_cat}'):
                                        await message.channel.send(f'Category "#{emojize(old_emoji)}-{old_cat}" was renamed to "#{replacement.emoji}-{old_cat}".')
                                        cats_old[old_cat] = demojize(replacement.emoji)
                                        cats('w', cats_old)
                                    else:
                                        await message.channel.send(f'Unexpected error happened while I tried to rename this channel. May the God forgive us.')
                                        break
                                else:
                                    break
                            else:
                                await message.channel.send('Mission failed. Try again next time!')
                                break
                cats('w', cats_old)



if __name__ == '__main__':
    client.run(settings['TOKEN'])

