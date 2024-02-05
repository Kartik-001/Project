import numpy as np
import random

# Constants
X = 'X'
O = 'O'
EMPTY = ' '
AI_PLAYER = O  # Change AI player to O
HUMAN_PLAYER = X  # Change human player to X

# Reward values
AI_WIN_REWARD = 1
HUMAN_WIN_REWARD = -1
TIE_REWARD = 0

# Q-learning parameters
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.9
EXPLORATION_PROBABILITY = 0.3

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def check_win(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True

    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True

    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True

    return False

def is_full(board):
    for row in board:
        if EMPTY in row:
            return False
    return True

def get_available_moves(board):
    moves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                moves.append((i, j))
    return moves

def make_ai_move(board, q_values):
    if random.uniform(0, 1) < EXPLORATION_PROBABILITY:
        return random.choice(get_available_moves(board))
    else:
        max_q = -float("inf")
        best_move = None
        for move in get_available_moves(board):
            i, j = move
            next_board = [row[:] for row in board]
            next_board[i][j] = AI_PLAYER
            next_state = tuple(tuple(row) for row in next_board)  # Corrected state representation
            q_value = q_values.get(((tuple(tuple(row) for row in board), move), 0))  # Corrected state representation
            if q_value > max_q:
                max_q = q_value
                best_move = move
        return best_move

def update_q_values(q_values, i, j, reward, board, move):
    q_values[(tuple(tuple(row) for row in board), move)] = q_values.get(((tuple(tuple(row) for row in board), move), 0)) + LEARNING_RATE * (reward + DISCOUNT_FACTOR * max(q_values.get(((tuple(tuple(row) for row in board), next_move), 0) for next_move in get_available_moves(board)) - q_values.get(((tuple(tuple(row) for row in board), move), 0))))  # Corrected state representation

def main():
    q_values = []
    for i in range(3):
        q_values.append([])
        for j in range(3):
            q_values[i].append({})

    print("Let's play Tic-Tac-Toe against AI!")
    while True:
        board = [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]
        current_player = HUMAN_PLAYER
        move_count = 0

        while True:
            if current_player == HUMAN_PLAYER:
                print_board(board)
                row, col = map(int, input(f"Player {current_player}, enter row and column (e.g., 1 2): ").split())
                if row < 1 or row > 3 or col < 1 or col > 3 or board[row - 1][col - 1] != EMPTY:
                    print("Invalid input. Try again.")
                    continue
                board[row - 1][col - 1] = HUMAN_PLAYER
            else:
                human_wins = check_win(board, HUMAN_PLAYER)
                if human_wins:
                    reward = HUMAN_WIN_REWARD
                elif is_full(board):
                    reward = TIE_REWARD
                else:
                    move = make_ai_move(board, q_values)
                    i, j = move
                    board[i][j] = AI_PLAYER

                if check_win(board, AI_PLAYER):
                    reward = AI_WIN_REWARD
                else:
                    reward = 0

                if current_player == AI_PLAYER:
                    update_q_values(q_values, i, j, reward, board, move)

            move_count += 1

            if check_win(board, current_player) or move_count == 9:
                print_board(board)
                if move_count == 9 and not check_win(board, current_player):
                    print("It's a tie!")
                else:
                    print(f"Player {current_player} wins!")
                break

            current_player = HUMAN_PLAYER if current_player == AI_PLAYER else AI_PLAYER

        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again != "yes":
            break

if __name__ == "__main__":
    main()
