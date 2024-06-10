import numpy as np
import math

# Constants for the Connect Four board
EMPTY = 0
PLAYER_X = 1
PLAYER_O = 2


def create_board():
    return np.zeros((6, 7), dtype=int)


def print_board(board):
    for row in reversed(range(6)):
        print("|", end="")
        for col in range(7):
            if board[row, col] == EMPTY:
                print("   ", end="|")
            elif board[row, col] == PLAYER_X:
                print(" X ", end="|")
            elif board[row, col] == PLAYER_O:
                print(" O ", end="|")
        print()
        # print("|---|" * 7)


def is_valid_move(board, col):
    # Check if the top row in the selected column is empty
    return board[5, col] == EMPTY


def make_move(board, col, player):
    for row in range(6):
        if board[row, col] == EMPTY:
            board[row, col] = player
            return


def get_possible_moves(board):
    return [col for col in range(7) if is_valid_move(board, col)]


def is_terminal(board):
    # Check for a winning state or a full board
    return (
        check_winner(board, PLAYER_X) or
        check_winner(board, PLAYER_O) or
        np.all(board != EMPTY)
    )


def evaluate(board):
    if check_winner(board, PLAYER_X):
        return 1
    elif check_winner(board, PLAYER_O):
        return -1
    else:
        return 0


def check_winner(board, player):
    # Check for a winning state in rows, columns, and diagonals
    for row in range(6):
        for col in range(4):
            if np.all(board[row, col:col+4] == player):
                return True

    for col in range(7):
        for row in range(3):
            if np.all(board[row:row+4, col] == player):
                return True

    for row in range(3):
        for col in range(4):
            if np.all(board[row:row+4, col:col+4].diagonal() == player):
                return True

    for row in range(3, 6):
        for col in range(4):
            board_val = np.flipud(board[row-3:row+1, col:col+4]).diagonal()
            if np.all(board_val == player):
                return True

    return False


def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or is_terminal(board):
        return evaluate(board)

    if maximizing_player:
        max_eval = -math.inf
        for move in get_possible_moves(board):
            new_board = board.copy()
            make_move(new_board, move, PLAYER_X)
            eval = minimax(new_board, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for move in get_possible_moves(board):
            new_board = board.copy()
            make_move(new_board, move, PLAYER_O)
            eval = minimax(new_board, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


def find_best_move(board, depth):
    best_move = None
    best_value = -math.inf

    for move in get_possible_moves(board):
        new_board = board.copy()
        make_move(new_board, move, PLAYER_X)
        move_value = minimax(new_board, depth - 1, -math.inf, math.inf, False)

        if move_value > best_value:
            best_value = move_value
            best_move = move

    return best_move


def main():
    # Example usage:
    board = create_board()
    print_board(board)

    while not is_terminal(board):
        # Player O's move
        o_move = find_best_move(board, depth=3)
        make_move(board, o_move, PLAYER_O)
        print("\nPlayer O's move:")
        print_board(board)

        if is_terminal(board):
            break

        # Player X's move
        x_move = int(input("Enter your move (column 0-6): "))
        while not is_valid_move(board, x_move):
            print("Invalid move. Try again.")
            x_move = int(input("Enter your move (column 0-6): "))

        make_move(board, x_move, PLAYER_X)
        print("\nYour move:")
        print_board(board)

    # Check the result of the game
    if check_winner(board, PLAYER_X):
        print("You win!")
    elif check_winner(board, PLAYER_O):
        print("Player O wins!")
    else:
        print("It's a draw!")


if __name__ == "__main__":
    main()
