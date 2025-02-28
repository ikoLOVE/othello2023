from typing import List, Union
import numpy as np
from IPython.display import clear_output
import time
import os
import random

BLACK = -1
WHITE = 1
EMPTY = 0

def init_board(N:int=8):
    # Initialize the board with an 8x8 numpy array
    board = np.zeros((N, N), dtype=int)
    # Set up the initial four stones
    C0 = N//2
    C1 = C0-1
    board[C1, C1], board[C0, C0] = WHITE, WHITE  # White
    board[C1, C0], board[C0, C1] = BLACK, BLACK  # Black
    return board

def count_board(board, piece=EMPTY):
    return np.sum(board == piece)

# Emoji representations for the pieces
BG_EMPTY = "\x1b[42m"
BG_RESET = "\x1b[0m"

stone_codes = [
    f'{BG_EMPTY}⚫️{BG_RESET}',
    f'{BG_EMPTY}🟩{BG_RESET}',
    f'{BG_EMPTY}⚪️{BG_RESET}',
]

def stone(piece):
    return stone_codes[piece+1]

def display_clear():
    os.system('clear')
    clear_output(wait=True)

BLACK_NAME=''
WHITE_NAME=''

def display_board(board, clear=True, sleep=0, black=None, white=None):
    """
    Display the Othello board with emoji representations.
    """
    global BLACK_NAME, WHITE_NAME
    if clear:
        clear_output(wait=True)
    if black:
        BLACK_NAME=black
    if white:
        WHITE_NAME=white
    for i, row in enumerate(board):
        for piece in row:
            print(stone(piece), end='')
        if i == 1:
            print(f'  {BLACK_NAME}')
        elif i == 2:
            print(f'   {stone(BLACK)}: {count_board(board, BLACK):2d}')
        elif i == 3:
            print(f'  {WHITE_NAME}')
        elif i == 4:
            print(f'   {stone(WHITE)}: {count_board(board, WHITE):2d}')
        else:
            print()  # New line after each row
    if sleep > 0:
        time.sleep(sleep)

def all_positions(board):
    N = len(board)
    return [(r, c) for r in range(N) for c in range(N)]

# Directions to check (vertical, horizontal)
directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]

def is_valid_move(board, row, col, player):
    # Check if the position is within the board and empty
    N = len(board)
    if row < 0 or row >= N or col < 0 or col >= N or board[row, col] != 0:
        return False

    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < N and 0 <= c < N and board[r, c] == -player:
            while 0 <= r < N and 0 <= c < N and board[r, c] == -player:
                r, c = r + dr, c + dc
            if 0 <= r < N and 0 <= c < N and board[r, c] == player:
                return True
    return False

def get_valid_moves(board, player):
    return [(r, c) for r, c in all_positions(board) if is_valid_move(board, r, c, player)]

def flip_stones(board, row, col, player):
    N = len(board)
    stones_to_flip = []
    for dr, dc in directions:
        directional_stones_to_flip = []
        r, c = row + dr, col + dc
        while 0 <= r < N and 0 <= c < N and board[r, c] == -player:
            directional_stones_to_flip.append((r, c))
            r, c = r + dr, c + dc
        if 0 <= r < N and 0 <= c < N and board[r, c] == player:
            stones_to_flip.extend(directional_stones_to_flip)
    return stones_to_flip

def display_move(board, row, col, player):
    stones_to_flip = flip_stones(board, row, col, player)
    board[row, col] = player
    display_board(board, sleep=0.3)
    for r, c in stones_to_flip:
        board[r, c] = player
        display_board(board, sleep=0.1)
    display_board(board, sleep=0.6)

def find_eagar_move(board, player):
    valid_moves = get_valid_moves(board, player)
    max_flips = 0
    best_result = None
    for r, c in valid_moves:
        stones_to_flip = flip_stones(board, r, c, player)
        if max_flips < len(stones_to_flip):
            best_result = (r, c)
            max_flips = len(stones_to_flip)
    return best_result




import sys

def display_board2(board, marks):
    """
    オセロ盤を表示する
    """
    global BLACK_NAME, WHITE_NAME
    clear_output(wait=True)
    for row, rows in enumerate(board):
        for col, piece in enumerate(rows):
            if (row, col) in marks:
                print(marks[(row,col)], end='')
            else:
                print(stone(piece), end='')
        if row == 1:
            print(f'  {BLACK_NAME}')
        elif row == 2:
            print(f'   {stone(BLACK)}: {count_board(board, BLACK):2d}')
        elif row == 3:
            print(f'  {WHITE_NAME}')
        elif row == 4:
            print(f'   {stone(WHITE)}: {count_board(board, WHITE):2d}')
        else:
            print()  # New line after each row
class OthelloAI(object):
    def __init__(self, face, name):
        self.face = face
        self.name = name

    def __repr__(self):
        return f"{self.face}{self.name}"

    def move(self, board: np.array, piece: int)->tuple[int, int]:
        valid_moves = get_valid_moves(board, piece)
        return valid_moves[0]

    def say(self, board: np.array, piece: int)->str:
        if count_board(board, piece) >= count_board(board, -piece):
            return 'やったー'
        else:
            return 'がーん'


import traceback

def board_play(player: OthelloAI, board, piece: int):
    skip_count=0
    display_board(board, sleep=0)
    if len(get_valid_moves(board, piece)) == 0:
        print(f"{player}は、置けるところがありません。スキップします。")
        skip_count+=1
        print(f"終了まで：{6-skip_count}手")
        if(skip_count>6):
            exit()
        return True
    try:
        start_time = time.time()
        r, c = player.move(board.copy(), piece)
        end_time = time.time()
    except:
        print(f"{player.face}{player.name}は、エラーを発生させました。反則まけ")
        traceback.print_exc()
        return False
    if not is_valid_move(board, r, c, piece):
        print(f"{player}が返した({r},{c})には、置けません。反則負け。")
        return False
    display_move(board, r, c, piece)
    return True

def comment(player1: OthelloAI, player2: OthelloAI, board):
    try:
        print(f"{player1}: {player1.say(board, BLACK)}")
    except:
        pass
    try:
        print(f"{player2}: {player2.say(board, WHITE)}")
    except:
        pass

def game(player1: OthelloAI, player2: OthelloAI,N=6):
    board = init_board(N)
    display_board(board, black=f'{player1}', white=f'{player2}')
    while count_board(board, EMPTY) > 0:
        if not board_play(player1, board, BLACK):
            break
        if not board_play(player2, board, WHITE):
            break
    comment(player1, player2, board)

class OchibiAI(OthelloAI):
    def __init__(self, face, name):
        self.face = face
        self.name = name


    def move(self, board: np.array, piece: int)->tuple[int, int]:
        valid_moves = get_valid_moves(board, piece)
        return valid_moves[0]

class iohana(OthelloAI):
    def __init__(self):
        self.face = '🌱'
        self.name = 'iohana'


    def monte_carlo_move(self, board, color: int, simulations: int = 100) -> tuple[int, int]:
        """
        モンテカルロ探索法に基づいて手を選ぶ
        """
        valid_moves = get_valid_moves(board, color)

        best_move = None
        best_score = float('-inf')

        for move in valid_moves:
            total_score = 0
            for _ in range(simulations):
                simulation_board = board.copy()
                make_move(simulation_board, move[0], move[1], color)
                total_score += self.monte_carlo_simulation(simulation_board, color)

            average_score = total_score / simulations

            if average_score > best_score:
                best_score = average_score
                best_move = move

        return best_move

    def monte_carlo_simulation(self, board, color: int) -> float:
        """
        モンテカルロシミュレーションの評価関数
        ここではランダムに手を選ぶだけの単純なものとしています。
        """
        return random.random()

    def alpha_beta_move(self, board, color: int, depth: int = 3) -> tuple[int, int]:
        """
        アルファベータ法に基づいて手を選ぶ
        """
        valid_moves = get_valid_moves(board, color)

        best_move = None
        alpha = float('-inf')
        beta = float('inf')

        for move in valid_moves:
            new_board = board.copy()
            make_move(new_board, move[0], move[1], color)
            score = self.alpha_beta_minimax(new_board, depth - 1, False, -color, alpha, beta)

            if score > alpha:
                alpha = score
                best_move = move

        return best_move

    def alpha_beta_minimax(self, board, depth, maximizing_player, color, alpha, beta) -> float:
        if depth == 0 or len(get_valid_moves(board, color)) == 0:
            return self.evaluate_board(board, color)

        valid_moves = get_valid_moves(board, color)
        if maximizing_player:
            for move in valid_moves:
                new_board = board.copy()
                make_move(new_board, move[0], move[1], color)
                alpha = max(alpha, self.alpha_beta_minimax(new_board, depth - 1, False, -color, alpha, beta))
                if beta <= alpha:
                    break
            return alpha
        else:
            for move in valid_moves:
                new_board = board.copy()
                make_move(new_board, move[0], move[1], color)
                beta = min(beta, self.alpha_beta_minimax(new_board, depth - 1, True, -color, alpha, beta))
                if beta <= alpha:
                    break
            return beta

    def evaluate_board(self, board, color) -> float:
        """
        ボードの評価関数
        ここでは簡単にコマの数を数えていますが、より高度な評価関数を実装することができます。
        """
        return count_board(board, color)

