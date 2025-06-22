from flask import Flask, render_template, request, redirect, url_for
import math

app = Flask(__name__)

# Game state
board = [' ' for _ in range(9)]
user_score = 0
computer_score = 0
draws = 0

# Check winner
def check_winner(brd, player):
    win_conditions = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    for condition in win_conditions:
        if all(brd[i] == player for i in condition):
            return True
    return False

# Draw condition
def is_draw():
    return ' ' not in board

# Get valid moves
def get_available_moves(brd):
    return [i for i, spot in enumerate(brd) if spot == ' ']

# Minimax logic
def minimax(brd, is_maximizing):
    if check_winner(brd, 'O'):
        return 1
    elif check_winner(brd, 'X'):
        return -1
    elif is_draw():
        return 0

    if is_maximizing:
        best_score = -math.inf
        for move in get_available_moves(brd):
            brd[move] = 'O'
            score = minimax(brd, False)
            brd[move] = ' '
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for move in get_available_moves(brd):
            brd[move] = 'X'
            score = minimax(brd, True)
            brd[move] = ' '
            best_score = min(score, best_score)
        return best_score

# AI move
def computer_move():
    best_score = -math.inf
    best_move = None
    for move in get_available_moves(board):
        board[move] = 'O'
        score = minimax(board, False)
        board[move] = ' '
        if score > best_score:
            best_score = score
            best_move = move
    if best_move is not None:
        board[best_move] = 'O'

# Routes
@app.route('/')
def index():
    winner = None
    if check_winner(board, 'X'):
        winner = 'You win!'
    elif check_winner(board, 'O'):
        winner = 'Computer wins!'
    elif is_draw():
        winner = 'It\'s a draw!'
    return render_template('index.html', board=board, winner=winner,
                           user_score=user_score, computer_score=computer_score, draws=draws)

@app.route('/move/<int:cell>')
def move(cell):
    if board[cell] == ' ' and not check_winner(board, 'X') and not check_winner(board, 'O'):
        board[cell] = 'X'
        if not check_winner(board, 'X') and not is_draw():
            computer_move()
    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    global board, user_score, computer_score, draws
    if check_winner(board, 'X'):
        user_score += 1
    elif check_winner(board, 'O'):
        computer_score += 1
    elif is_draw():
        draws += 1
    board = [' ' for _ in range(9)]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
