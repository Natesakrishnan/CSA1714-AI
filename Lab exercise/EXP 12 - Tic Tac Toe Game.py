<<<<<<< HEAD

board = [' ' for _ in range(9)]

def display_board():
    print()
    print(board[0], '|', board[1], '|', board[2])
    print('--+---+--')
    print(board[3], '|', board[4], '|', board[5])
    print('--+---+--')
    print(board[6], '|', board[7], '|', board[8])
    print()

def check_winner(player):
    win_positions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]

    for a, b, c in win_positions:
        if board[a] == board[b] == board[c] == player:
            return True
    return False

def tic_tac_toe():
    player = 'X'

    for turn in range(9):
        display_board()
        print("Player", player)

        try:
            position = int(input("Enter position (1-9): ")) - 1
        except ValueError:
            print("Invalid input! Enter a number from 1 to 9.")
            continue

        if position < 0 or position > 8 or board[position] != ' ':
            print("Invalid position! Try again.")
            continue

        board[position] = player

        if check_winner(player):
            display_board()
            print("Player", player, "wins!")
            return

        player = 'O' if player == 'X' else 'X'

    display_board()
    print("Match Draw!")

tic_tac_toe()
=======

board = [' ' for _ in range(9)]

def display_board():
    print()
    print(board[0], '|', board[1], '|', board[2])
    print('--+---+--')
    print(board[3], '|', board[4], '|', board[5])
    print('--+---+--')
    print(board[6], '|', board[7], '|', board[8])
    print()

def check_winner(player):
    win_positions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]

    for a, b, c in win_positions:
        if board[a] == board[b] == board[c] == player:
            return True
    return False

def tic_tac_toe():
    player = 'X'

    for turn in range(9):
        display_board()
        print("Player", player)

        try:
            position = int(input("Enter position (1-9): ")) - 1
        except ValueError:
            print("Invalid input! Enter a number from 1 to 9.")
            continue

        if position < 0 or position > 8 or board[position] != ' ':
            print("Invalid position! Try again.")
            continue

        board[position] = player

        if check_winner(player):
            display_board()
            print("Player", player, "wins!")
            return

        player = 'O' if player == 'X' else 'X'

    display_board()
    print("Match Draw!")

tic_tac_toe()
>>>>>>> origin/main
