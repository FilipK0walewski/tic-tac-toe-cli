import copy
import os
import random
import time

from typing import List, Union


class Game:

    def __init__(self):
        self.running = True
        self.playing = False
        self.ai_game = False

        self.scoreboard = [None] * 9
        self.screen = self.make_screen()
        self.sign = 'X'
        self.ai_sign = 'O'

        self.messages = []

    def make_screen(self) -> List[List[Union[str]]]:
        lines = []
        for i in range(13):
            line = (['# '] + ['  '] * 3) * 3 + ['# ']
            if i % 4 == 0:
                line = ['# '] * 13
            lines.append(line)

        return lines

    def update_screen(self):
        n = 0
        for i in (2, 6, 10):
            for j in (2, 6, 10):
                sign = f'{n+1} '
                if self.scoreboard[n] is not None:
                    color = '\033[35m' if self.scoreboard[n] == 'X' else '\033[36m'
                    sign = f'{color}{self.scoreboard[n]}\033[0m '
                self.screen[i][j] = sign
                n += 1
                
    def draw_screen(self):
        os.system('clear')
        self.update_screen()
        for line in self.screen:
            print(''.join(line))
        for message in self.messages:
            print(message)
        self.messages.clear()

    def reset_game_state(self):
        self.scoreboard = [None] * 9
        tmp = random.choice([0, 1])
        if self.ai_game is True:
            self.sign = 'X'
            if tmp == 0:
                self.ai_move()
                self.messages.append('Computer made first move.')
        else:
            self.sign == 'X' if tmp == 0 else 'O'

    def check_if_game_ends(self, scoreboard: list[str]) -> Union[str, None]:
        for p_0, p_1, p_2 in [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]:
            if scoreboard[p_0] is None:
                continue
            if scoreboard[p_0] == scoreboard[p_1] and  scoreboard[p_1] == scoreboard[p_2]:
                return scoreboard[p_0]

        if None not in scoreboard:
            return 'DRAW'

        return None

    def switch_turn(self):
        self.sign = 'O' if self.sign == 'X' else 'X'

    def minimax(self, scoreboard: list[str], is_maximizing: bool):
        winner = self.check_if_game_ends(scoreboard)
        if winner == 'DRAW':
            return 0
        elif winner == self.ai_sign:
            return 1
        elif winner == self.sign:
            return -1

        if is_maximizing is True:
            best_score = float('-inf')
            for i in range(9):
                if scoreboard[i] is None:
                    scoreboard[i] = self.ai_sign
                    score = self.minimax(scoreboard, False)
                    scoreboard[i] = None
                    best_score = max(score, best_score)
            return best_score

        elif is_maximizing is False:
            best_score = float('inf')
            for i in range(9):
                if scoreboard[i] is None:
                    scoreboard[i] = self.sign
                    score = self.minimax(scoreboard, True)
                    scoreboard[i] = None
                    best_score = min(score, best_score)

            return best_score

    def ai_move(self):
        best_move, best_score = None, float('-inf')
        for i in range(9):
            if self.scoreboard[i] is None:
                self.scoreboard[i] = self.ai_sign
                score = self.minimax(self.scoreboard, False)
                self.scoreboard[i] = None
                if score > best_score:
                    best_score = score
                    best_move = i
        
        if best_move is None:
            return
        self.scoreboard[best_move] = self.ai_sign

    def game_loop(self):
        self.reset_game_state()
        while self.playing is True:
            self.draw_screen()

            user_input = input(f'{self.sign} move: ')
            if user_input.isnumeric() is False:
                self.messages.append('Invalid input.')
                continue

            user_input = int(user_input) - 1
            if user_input > 8 or user_input < 0:
                self.messages.append('Invalid input.')
                continue
            
            if self.scoreboard[user_input] is not None:
                self.messages.append('Can not do that move.')
                continue
            
            self.scoreboard[user_input] = self.sign
            if self.ai_game is True:
                self.ai_move()
            else:
                self.switch_turn()

            winner = self.check_if_game_ends(self.scoreboard)
            if winner is not None:
                if winner == 'DRAW':
                    self.messages.append('DRAW!')
                else:
                    self.messages.append(f'{winner} wins the game!')
                self.playing = False
                self.ai_game = False
                self.draw_screen()
            
    def menu_loop(self):
        while self.running is True and self.playing is False:
            user_input = input('\n1. Play vs human\n2. Play vs computer\n3. Quit game\nYour choice: ')
            if user_input == '1':
                self.playing = True
                self.ai_game = False
            elif user_input == '2':
                self.playing = True
                self.ai_game = True
            elif user_input == '3':
                self.playing = False
                self.running = False
            else:
                print('Invalid input.')

    def main_loop(self):
        while self.running is True:
            self.game_loop()
            self.menu_loop()

        print('quiting game...')
        time.sleep(3)


if __name__ == '__main__':
    os.system('clear')
    Game().main_loop()
