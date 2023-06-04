class TicTacToe:
    def __init__(self, bot):
        self.maps = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.victories = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
        self.win = ""
        self.bot = bot
        self.game_over = False
        self.human = True

    def print_board(self):
        return f'```\n {self.maps[0]} | {self.maps[1]} | {self.maps[2]} \n---+---+---\n {self.maps[3]} | {self.maps[4]} | {self.maps[5]} \n---+---+---\n {self.maps[6]} | {self.maps[7]} | {self.maps[8]} \n```'

    def make_turn(self, turn, symbol):
        ind = self.maps.index(turn)
        self.maps[ind] = symbol

    def get_result(self):
        self.win = ""

        for i in self.victories:
            if self.maps[i[0]] == "X" and self.maps[i[1]] == "X" and self.maps[i[2]] == "X":
                self.win = "X"
                break
            if self.maps[i[0]] == "O" and self.maps[i[1]] == "O" and self.maps[i[2]] == "O":
                self.win = "O"
                break

        if self.win == "":
            count = 0
            for elem in self.maps:
                if elem not in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                    count += 1
            if count == 9:
                self.win = "Ничья"

        return self.win

    def check_line(self, sum_0, sum_x):
        step = ""
        for line in self.victories:
            o = 0
            x = 0

            for j in range(0, 3):
                if self.maps[line[j]] == "O":
                    o = o + 1
                if self.maps[line[j]] == "X":
                    x = x + 1

            if o == sum_0 and x == sum_x:
                for j in range(0, 3):
                    if self.maps[line[j]] != "O" and self.maps[line[j]] != "X":
                        step = self.maps[line[j]]

        return step

    def find_best_step(self):
        step = self.check_line(2, 0)

        if step == "":
            step = self.check_line(0, 2)

        if step == "":
            step = self.check_line(1, 0)

        if step == "":
            if self.maps[4] != "X" and self.maps[4] != "O":
                step = 5

        if step == "":
            if self.maps[0] != "X" and self.maps[0] != "O":
                step = 1

        return step


def play_tic_tac_toe_with_bot():
    game_over = False
    human = True
    game = TicTacToe(bot=True)

    while not game_over:
        game.print_board()

        if human:
            symbol = "X"
            step = int(input("Человек, ваш ход: "))
        else:
            print("Компьютер делает ход: ")
            symbol = "O"
            step = game.find_best_step()

        if step != "":
            game.make_turn(step, symbol)
            win = game.get_result()
            if win != "":
                game_over = True
            else:
                game_over = False
        else:
            game_over = True

        human = not human

    game.print_board()
    if game.win != '':
        print("Победил", game.win)
    if game.win == '':
        print("Ничья!")


def play_tic_tac_toe_with_human():
    game_over = False
    human = True
    game = TicTacToe(bot=False)

    while not game_over:
        game.print_board()

        if human:
            symbol = "X"
            step = int(input("Игрок 1, ваш ход: "))
        else:
            symbol = "O"
            step = int(input("Игрок 2, ваш ход: "))

        if step != "":
            game.make_turn(step, symbol)
            win = game.get_result()
            if win != "":
                game_over = True
            else:
                game_over = False
        else:
            game_over = True

        human = not human

    game.print_board()
    if game.win != '':
        print("Победил", game.win)
    if game.win == '':
        print("Ничья!")

# play_tic_tac_toe_with_bot()
# play_tic_tac_toe_with_human()
