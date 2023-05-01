import discord
from discord.ext import commands
from config import settings
import random
import zipfile
import os
import asyncio

COIN = ['Орёл', 'Решка']
ARCHIVE_MOD = False

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=settings['prefix'], intents=intents)


@bot.command()
async def roll_dice(ctx):
    await ctx.reply(random.randint(1, 6))


@bot.command()
async def coin_flip(ctx):
    await ctx.reply(random.choice(COIN))


@bot.command()
async def generate_number(ctx, x, y):
    await ctx.reply(random.randint(int(x), int(y)))


@bot.command()
async def start_archive(message):
    global ARCHIVE_MOD
    ARCHIVE_MOD = True


@bot.command()
async def stop_archive(message):
    global ARCHIVE_MOD
    ARCHIVE_MOD = False


@bot.event
async def on_message(message):
    global ARCHIVE_MOD

    if message.author == bot.user:
        return

    if ARCHIVE_MOD:
        if message.content == "/stop_archive":
            with zipfile.ZipFile('data/archive.zip', mode='a') as archive:
                archive.write("messages/text.txt")

            await message.channel.send(file=discord.File(r'data/archive.zip'))

            os.remove("messages/text.txt")
            os.remove('data/archive.zip')

        else:
            for attachment in message.attachments:
                with zipfile.ZipFile('data/archive.zip', mode='a') as archive:
                    await attachment.save(f'images/{attachment.filename}')
                    archive.write(f'images/{attachment.filename}')
                    os.remove(f'images/{attachment.filename}')

            if message.content != "":
                with open("messages/text.txt", "a") as text:
                    text.write(f'\n{message.content}')
    await bot.process_commands(message)

bot.run(settings['token'])
