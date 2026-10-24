
# Tic Tac Toe using Alpha-Beta Pruning

board = [' '] * 9

winning_positions = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
]

def check_winner():
    for a, b, c in winning_positions:
        if board[a] == board[b] == board[c] != ' ':
            return board[a]
    return None

def minimax(alpha, beta, is_maximizing):
    winner = check_winner()

    if winner == 'X':
        return 1
    if winner == 'O':
        return -1
    if ' ' not in board:
        return 0

    if is_maximizing:
        best_score = -float('inf')

        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(alpha, beta, False)
                board[i] = ' '

                best_score = max(best_score, score)
                alpha = max(alpha, best_score)

                if beta <= alpha:
                    break

        return best_score

    else:
        best_score = float('inf')

        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax(alpha, beta, True)
                board[i] = ' '

                best_score = min(best_score, score)
                beta = min(beta, best_score)

                if beta <= alpha:
                    break

        return best_score

def ai_move():
    best_score = -float('inf')
    best_move = None
    alpha = -float('inf')
    beta = float('inf')

    for i in range(9):
        if board[i] == ' ':
            board[i] = 'X'
            score = minimax(alpha, beta, False)
            board[i] = ' '

            if score > best_score:
                best_score = score
                best_move = i

            alpha = max(alpha, best_score)

    if best_move is not None:
        board[best_move] = 'X'

def display_board():
    print()
    for i in range(0, 9, 3):
        print(" | ".join(board[i:i + 3]))
        if i < 6:
            print("--+---+--")
    print()

def play_game():
    print("TIC TAC TOE - ALPHA-BETA PRUNING")
    print("You are O; Computer is X.")
    print("Positions:")
    print("1 | 2 | 3")
    print("--+---+--")
    print("4 | 5 | 6")
    print("--+---+--")
    print("7 | 8 | 9")

    while True:
        ai_move()
        print("\nComputer's move:")
        display_board()

        if check_winner() == 'X':
            print("Computer wins!")
            break

        if ' ' not in board:
            print("Match Draw!")
            break

        while True:
            try:
                position = int(input("Enter your position (1-9): ")) - 1

                if 0 <= position < 9 and board[position] == ' ':
                    board[position] = 'O'
                    break

                print("Invalid or occupied position. Try again.")

            except ValueError:
                print("Please enter a number from 1 to 9.")

        print("\nYour move:")
        display_board()

        if check_winner() == 'O':
            print("You win!")
            break

        if ' ' not in board:
            print("Match Draw!")
            break

play_game()

