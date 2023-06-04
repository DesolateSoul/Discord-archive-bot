import discord
from discord.ext import commands
from config import settings
from TicTacToe import TicTacToe
import random
import zipfile
import os
import asyncio

COIN = ['Орёл', 'Решка']
ARCHIVE_MOD = False
GAME_MOD = False
GAME = TicTacToe(False)

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


@bot.command()
async def play_tic_tac_toe_bot(message):
    global GAME_MOD
    global GAME
    GAME_MOD = True


@bot.command()
async def play_tic_tac_toe_human(message):
    global GAME_MOD
    global GAME
    GAME_MOD = True


@bot.event
async def on_message(message):
    global ARCHIVE_MOD
    global GAME_MOD
    global GAME

    if message.author == bot.user:
        return

    if ARCHIVE_MOD:
        if message.content == "/stop_archive":
            with zipfile.ZipFile('data/archive.zip', mode='a') as archive:
                archive.write("messages/text.txt")

            await message.channel.send(file=discord.File(r'data/archive.zip'))

            if os.path.exists("messages/text.txt"):
                os.remove("messages/text.txt")
            if os.path.exists("images/text.txt"):
                os.remove("images/text.txt")
            if os.path.exists('data/archive.zip'):
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

    if GAME_MOD or (message.content in ["/play_tic_tac_toe_bot", "/play_tic_tac_toe_human"]):
        if message.content in ["/play_tic_tac_toe_bot", "/play_tic_tac_toe_human"]:
            if message.content == "/play_tic_tac_toe_bot":
                GAME = TicTacToe(bot=True)
            else:
                GAME = TicTacToe(bot=False)
            await message.reply("Game start")
            await message.reply(GAME.print_board())
        else:
            if not GAME.game_over:

                win = GAME.get_result()

                if win == "":
                    if GAME.human:
                        symbol = "X"
                        step = int(message.content)
                        GAME.make_turn(step, symbol)

                    if not GAME.human:
                        symbol = "O"
                        step = int(message.content)
                        GAME.make_turn(step, symbol)

                    if not GAME.bot:
                        GAME.human = not GAME.human

                win = GAME.get_result()

                if win == "" and GAME.bot:
                    symbol = "O"
                    step = GAME.find_best_step()
                    if step == "":
                        GAME.game_over = True
                    else:
                        await message.reply("Компьютер делает ход: ")
                        GAME.make_turn(step, symbol)

                await message.reply(GAME.print_board())

                win = GAME.get_result()

                if win != "":
                    GAME.game_over = True

            if GAME.win != "" and GAME.win != "Ничья":
                await message.reply(f"Победил {GAME.win}")
                GAME_MOD = False

            if GAME.win == "Ничья" and GAME.game_over:
                await message.reply(f"Ничья!")
                GAME_MOD = False

    await bot.process_commands(message)

bot.run(settings['token'])
