def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)


print_board([[" " for _ in range(3)] for _ in range(3)])