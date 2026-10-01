def is_safe(board, row, col):
    for i in range(row):
        if board[i] == col:
            return False

    for i in range(row):
        if board[i] - i == col - row:
            return False

    for i in range(row):
        if board[i] + i == col + row:
            return False

    return True


def solve_queens(board, row):
    if row == 8:
        return True

    for col in range(8):

        if is_safe(board, row, col):
            board[row] = col

            if solve_queens(board, row + 1):
                return True

            board[row] = -1

    return False


def print_board(board):
    for row in range(8):
        for col in range(8):
            if board[row] == col:
                print("Q", end=" ")
            else:
                print(".", end=" ")
        print()

board = [-1] * 8

if solve_queens(board, 0):
    print("Solution for 8-Queens Problem:")
    print_board(board)
else:
    print("No solution exists.")
