# MODULES
import random
import pygame, sys
import numpy as np

# initializes pygame
pygame.init()

# ---------
# CONSTANTS
# ---------
WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 15
WIN_LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = 200
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55
# rgb: red green blue
RED = (255, 0, 0)
BG_COLOR = (207, 159, 255)
LINE_COLOR = (128, 0, 128)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

# ------
# SCREEN
# ------
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption( 'TIC TAC TOE' )
screen.fill( BG_COLOR )

# -------------
# CONSOLE BOARD
# -------------
board = np.zeros( (BOARD_ROWS, BOARD_COLS) )
board = [[' ' for _ in range(3)] for _ in range(3)]


def draw_lines():
    pygame.draw.line( screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH )
    pygame.draw.line( screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH )
    pygame.draw.line( screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH )
    pygame.draw.line( screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH )
# Function to print the Tic-Tac-Toe board
def print_board(board):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'O':
                pygame.draw.circle( screen, CIRCLE_COLOR, (int( col * SQUARE_SIZE + SQUARE_SIZE//2 ), int( row * SQUARE_SIZE + SQUARE_SIZE//2 )), CIRCLE_RADIUS, CIRCLE_WIDTH )
            elif board[row][col] == 'X':
                pygame.draw.line( screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH )	
                pygame.draw.line( screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH )

def restart():
    screen.fill( BG_COLOR )
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = ' '

def draw_vertical_winning_line(col, player):
    posX = col * SQUARE_SIZE + SQUARE_SIZE//2
    if player == 'O':
        color = CIRCLE_COLOR
    elif player == 'X':
        color = CROSS_COLOR
    pygame.draw.line( screen, color, (posX, 15), (posX, HEIGHT - 15), LINE_WIDTH )

def draw_horizontal_winning_line(row, player):
    posY = row * SQUARE_SIZE + SQUARE_SIZE//2
    if player == 'O':
        color = CIRCLE_COLOR
    elif player == 'X':
        color = CROSS_COLOR
    pygame.draw.line( screen, color, (15, posY), (WIDTH - 15, posY), WIN_LINE_WIDTH )

def draw_asc_diagonal(player):
    if player == 'O':
        color = CIRCLE_COLOR
    elif player == 'X':
        color = CROSS_COLOR
    pygame.draw.line( screen, color, (15, HEIGHT - 15), (WIDTH - 15, 15), WIN_LINE_WIDTH )

def draw_desc_diagonal(player):
    if player == 'O':
        color = CIRCLE_COLOR
    elif player == 'X':
        color = CROSS_COLOR
    pygame.draw.line( screen, color, (15, 15), (WIDTH - 15, HEIGHT - 15), WIN_LINE_WIDTH )
# Function to check if the current player has won'''

def check_winner(player):
    for col in range(3):
        if (board[0][col] == player and board[1][col] == player and board[2][col] == player):
            draw_vertical_winning_line(col, player)
            return True
    for row in range(3):
        if (board[row][0] == player and board[row][1] == player and board[row][2] == player):
            draw_horizontal_winning_line(row, player)
            return True
    if (board[2][0] == player and board[1][1] == player and board[0][2] == player):
        draw_asc_diagonal(player)
        return True
    if (board[0][0] == player and board[1][1] == player and board[2][2] == player):
        draw_desc_diagonal(player)
        return True
    return False

def mark_square(row, col, player):
	board[row][col] = player

def available_square(row, col):
	return board[row][col] == ' '

# Function to check if the board is full
def is_board_full():
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			if board[row][col] == ' ':
				return False
	return True

# Function to evaluate the current state of the board for the AI player
def check_win(t_board, player):
    # Check rows and columns
    for i in range(3):
        if all(t_board[i][j] == player for j in range(3)) or all(t_board[j][i] == player for j in range(3)):
            return True
    # Check diagonals
    if all(t_board[i][i] == player for i in range(3)) or all(t_board[i][2 - i] == player for i in range(3)):
        return True
    return False
def evaluate(t_board):
    if check_win(t_board,'X'):
        return -1
    elif check_win(t_board,'O'):
        return 1
    elif is_board_full():
        return 0
    else:
        return None

# Minimax function with Alpha-Beta Pruning
def minimax(board, depth, maximizing_player, alpha, beta):
    t_board = board[:][:]
    result = evaluate(t_board)

    if result is not None: 
        return result

    if maximizing_player:
        max_eval = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    eval = minimax(t_board, depth + 1, False, alpha, beta)
                    board[i][j] = ' '

                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)

                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    eval = minimax(t_board, depth + 1, True, alpha, beta)
                    board[i][j] = ' '

                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)

                    if beta <= alpha:
                        break
        return min_eval

# Function to find the best move for the AI player using Minimax with Alpha-Beta Pruning
def find_best_move(board):
    best_val = float('-inf')
    best_move = None

    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                move_val = minimax(board, 0, False, float('-inf'), float('inf'))
                board[i][j] = ' '

                if move_val > best_val:
                    best_move = (i, j)
                    best_val = move_val

    return best_move

# Function to play the Tic-Tac-Toe game


player = 'X'

while True:
    
    game_over = False
    
    for event in pygame.event.get():
        draw_lines()
        print_board(board)
        if event.type == pygame.QUIT:
            sys.exit()
        
        if player=='X':
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX = event.pos[0] # x
                mouseY = event.pos[1] # y
                clicked_row = int(mouseY // SQUARE_SIZE)
                clicked_col = int(mouseX // SQUARE_SIZE)
                if available_square( clicked_row, clicked_col ):
                    mark_square( clicked_row, clicked_col, player )
                    if check_winner('X'):
                        game_over = True
                    player = 'O'
            
            print_board(board)
            pygame.display.update()
            
        
        elif player=='O':
            
            best_move = find_best_move(board)
          
            print_board(board)
            mark_square( best_move[0], best_move[1], player )
            if check_winner('O'):
                        game_over = True            
            print_board(board)
            player = 'X'
            
            pygame.display.update()
        
        if game_over:
            pygame.time.wait(2000)
            restart()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
                player = 'X'
                game_over = False
    
    flag=0
    for i in range (3):
        for j in range(3):
            if board[i][j]==' ':
                flag+=1
    if flag == 0:
        restart()       
            
    pygame.display.update()


