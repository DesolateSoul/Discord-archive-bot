import discord
from discord.ext import commands
from config import settings
from TicTacToe import TicTacToe
import random
import zipfile
import os

INFO = '''Функция /roll_dice. Бросок игральной кости. Выдаёт случайное число от 1 до 6. 
Функция /coin_flip. Бросок монеты. Выдаёт одно из названий сторон монеты.
Функция /generate_number x y. Генератор случайных целых чисел в диапазоне от x до y.
Функции /start_archive и /stop_archive. После ввода первой функции бот автоматически запишет все дальнейшие отправленные пользователями файлы в архив zip, после ввода второй функции, архив отправляется в чат.
Функции /play_tic_tac_toe_bot и /play_tic_tac_toe_human, /resign. Запускают игру в крестики нолики с ботом и с человеком (локально) соответственно, последняя предназначена для преждевременного прекращения игры. '''

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


@bot.command()
async def resign(message):
    global GAME_MOD
    GAME_MOD = False


@bot.command()
async def info(message):
    global INFO
    await message.reply(INFO)


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
            if os.path.exists("files/text.txt"):
                os.remove("files/text.txt")
            if os.path.exists('data/archive.zip'):
                os.remove('data/archive.zip')

        else:
            for attachment in message.attachments:
                with zipfile.ZipFile('data/archive.zip', mode='a') as archive:
                    await attachment.save(f'files/{attachment.filename}')
                    archive.write(f'files/{attachment.filename}')
                    os.remove(f'files/{attachment.filename}')

            if message.content != "":
                with open("messages/text.txt", "a") as text:
                    text.write(f'\n{message.content}')

    if GAME_MOD or (message.content in ["/play_tic_tac_toe_bot", "/play_tic_tac_toe_human", "/resign"]):
        if message.content in ["/play_tic_tac_toe_bot", "/play_tic_tac_toe_human", "/resign"]:
            if message.content == "/play_tic_tac_toe_bot":
                GAME = TicTacToe(bot=True)
                await message.reply("Началась игра с ботом.")
                await message.reply(GAME.print_board())
            elif message.content == "/play_tic_tac_toe_human":
                GAME = TicTacToe(bot=False)
                await message.reply("Началась игра с человеком.")
                await message.reply(GAME.print_board())

            if message.content == "/resign":
                if GAME.bot:
                    await message.reply("Победил O.")
                else:
                    if GAME.human:
                        await message.reply("Победил O.")
                    else:
                        await message.reply("Победил X.")
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

            elif GAME.win == "Ничья" or GAME.game_over:
                await message.reply(f"Ничья!")
                GAME_MOD = False

    await bot.process_commands(message)

bot.run(settings['token'])
