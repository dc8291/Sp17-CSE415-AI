'''Daniel Chai and Etai Liokumovich
CSE 415 Baroque Chess Player
May 8th, 2017 '''

import time

BLACK = 0
WHITE = 1

INIT_TO_CODE = {'p': 2, 'P': 3, 'c': 4, 'C': 5, 'l': 6, 'L': 7, 'i': 8, 'I': 9,
                'w': 10, 'W': 11, 'k': 12, 'K': 13, 'f': 14, 'F': 15, '-': 0}

CODE_TO_INIT = {0: '-', 2: 'p', 3: 'P', 4: 'c', 5: 'C', 6: 'l', 7: 'L', 8: 'i', 9: 'I',
                10: 'w', 11: 'W', 12: 'k', 13: 'K', 14: 'f', 15: 'F'}


def who(piece): return piece % 2


def parse(bs):  # bs is board string
    '''Translate a board string into the list of lists representation.'''
    b = [[0, 0, 0, 0, 0, 0, 0, 0] for r in range(8)]
    rs9 = bs.split("\n")
    rs8 = rs9[1:]  # eliminate the empty first item.
    for iy in range(8):
        rss = rs8[iy].split(' ')
        for jx in range(8):
            b[iy][jx] = INIT_TO_CODE[rss[jx]]
    return b


INITIAL = parse('''
c l i w k i l f
p p p p p p p p
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
P P P P P P P P
F L I W K I L C
''')


class BC_state:
    def __init__(self, old_board=INITIAL, whose_move=WHITE):
        new_board = [r[:] for r in old_board]
        self.board = new_board
        self.whose_move = whose_move

    def __repr__(self):
        s = ''
        for r in range(8):
            for c in range(8):
                s += CODE_TO_INIT[self.board[r][c]] + " "
            s += "\n"
        if self.whose_move == WHITE:
            s += "WHITE's move"
        else:
            s += "BLACK's move"
        s += "\n"
        return s

def makeMove(currentState, currentRemark, timelimit):
    move = 'GG'
    newRemark = "Your Move!"
    start_time = time.time()
    newState = minimax(currentState.board, currentState.whose_move, 2)
    print(time.time() - start_time)
    return [[move, newState[0]], newRemark]


def minimax(board, whoseMove, plyLeft):
    new_state = BC_state(board, whoseMove)
    if plyLeft == 0:
        return [new_state, staticEval(board)]
    if whoseMove == 1:
        provisional = -10000000
    else:
        provisional = 10000000
    if whoseMove == 1:
        tempWhoseMove = 0
    else:
        tempWhoseMove = 1
    for s in generateMove(board, whoseMove):
        newVal = minimax(s, tempWhoseMove, plyLeft - 1)
        if (whoseMove == 1 and newVal[1] > provisional) or (whoseMove == 0 and newVal[1] < provisional):
            provisional = newVal[1]
            new_state.board = s
            new_state.whose_move = tempWhoseMove
    return [new_state, provisional]

def generateMove(board, whose_move):
    L = []
    for i in range(8):
        for j in range(8):
            piece = board[i][j]  # Look at a piece
            if piece != 0:  # If it isn't empty
                piece_color = piece % 2  # Look at its color
                if piece_color == whose_move:  # If the color matches whose turn it is
                    for x in range(8):
                        for y in range(8):
                            try:
                                temp_board = [r[:] for r in board]
                                new_board = make_a_move(temp_board, [i, j], [x, y])
                                L.append(new_board)
                            except:
                                continue
    return L


def nickname():
    return "Test"


def introduce():
    return "I'm Test. I am being tested."


def prepare(player2Nickname):
    return "Prepare to die!"


lateGame = False  # Whether ten pieces have been captured

# Takes in a state
# Calculates the current state of the board
# Higher number means better for white, lower mean better for black
# Returns an integer
def staticEval(board):
    sum = 0
    for i in range(8):
        for j in range(8):
            multiplier = 1
            piece = board[i][j]  # INIT_TO_CODE = {'p': 2, 'P': 3, 'c': 4, 'C': 5, 'l': 6, 'L': 7, 'i': 8, 'I': 9,
            # 'w': 10, 'W': 11, 'k': 12, 'K': 13, 'f': 14, 'F': 15, '-': 0}
            sum += PIECE_EVALUATION[piece]
            piece_location = i * 8 + j
            if piece % 2 == 0:  # If piece is black
                multiplier = -1
                piece_location = 63 - piece_location  # Inverting the board for black
            piece_id = piece // 2
            if piece_id == 1:  # If it is a Pincer
                sum += PINCER_BOARD[piece_location] * multiplier  # Looks the Pincer board evaluation
                nearby = surrounding_pieces(i, j, board, piece_id, piece)  # Calculate nearby pieces
                sum += nearby * 5 * multiplier
            if piece_id == 2:  # If it is a Coordinator
                power = potential(i, j, board, piece)
                sum += power * 50 * multiplier
            if piece_id == 3:  # If it is a Leaper
                sum += LEAPER_BOARD[piece_location] * multiplier
                power = potential(i, j, board, piece)
                sum += power * 50 * multiplier
            if piece_id == 4:  # If it is an Imitator
                nearby = surrounding_pieces(i, j, board, piece_id, piece)
                sum += nearby * multiplier // 10
            if piece_id == 5:  # If it is a Withdrawer
                sum += WITHDRAWER_BOARD[piece_location] * multiplier
            if piece_id == 6:  # If it is a King
                nearby = surrounding_pieces(i, j, board, piece_id, piece)
                late_factor = 20
                if lategame(board):
                    sum += KING_BOARD_LATE[piece_location] * multiplier
                    late_factor = 60
                else:
                    sum += KING_BOARD_EARLY[piece_location] * multiplier
                sum += nearby * late_factor * multiplier
            if piece_id == 7:  # If it is a Freezer
                nearby = surrounding_pieces(i, j, board, piece_id, piece)
                sum += nearby * 100 * multiplier
    return sum


# Takes in the current board state
# Calculates the number of pieces left
# returns whether current state is late game (10 pieces or less)
def lategame(board):
    number = 0
    for i in range(8):
        for j in range(8):
            if board[i][j] != 0:
                number += 1
                if number > 10:
                    return False
    return True


# Takes in the current board state and the piece
# Finds where your ally king is
# Returns the coordinate in [x, y] form
def findKing(board, piece_number):
    color = piece_number % 2  # Determine the color of the piece
    if color == 1:
        king = 13
    else:
        king = 12
    for i in range(8):
        for j in range(8):
            if board[i][j] == king:
                return [i, j]
    return [-1, -1]


# Takes in the two coordinates i and j, current board state, and the code of the piece
# Calculates potential for leaper and coordinator
# For leaper, it is how many enemies are currently capturable
# For Coordinator, it's how many empty squares there are
# Returns that number
def potential(i, j, board, piece_number):
    Leaper_can_capture = 0  # Number of pieces that can be captured by the leaper
    Coordinator_space = 0
    king = findKing(board, piece_number)
    kingi = king[0]
    kingj = king[1]
    if i != 0:
        tempi = i
        while tempi > 1:  # Checking above
            above = board[tempi - 1][j]
            if above == 0:  # If above is empty
                tempi -= 1
                if kingi != -1 and tempi != kingi and j != kingj:
                    Coordinator_space += 1
            elif isEnemy(piece_number, above):  # If above is enemy
                if board[tempi - 2][j] == 0:  # enemy is capturable
                    Leaper_can_capture += 1
                    break
                else:
                    tempi -= 1
            else:  # If above is an ally
                break
        if j != 0:  # if piece is not left
            tempj = j
            tempi = i
            while tempi > 1 and tempj > 1:  # Checking top left
                top_left = board[tempi - 1][tempj - 1]
                if top_left == 0:  # If top left is empty
                    tempi -= 1
                    tempj -= 1
                    if kingi != -1 and tempi != kingi and tempj != kingj:
                        Coordinator_space += 1
                elif isEnemy(piece_number, top_left):  # If top left is enemy
                    if board[tempi - 2][tempj - 2] == 0:
                        Leaper_can_capture += 1
                        break
                    else:
                        tempi -= 1
                        tempj -= 1
                else:  # If top left is an ally
                    break
        if j != 7:  # if piece is not left
            tempj = j
            tempi = i
            while tempi > 1 and tempj < 6:  # Checking top right
                top_right = board[tempi - 1][tempj + 1]
                if top_right == 0:  # If top left is empty
                    tempi -= 1
                    tempj += 1
                    if kingi != -1 and tempi != kingi and tempj != kingj:
                        Coordinator_space += 1
                elif isEnemy(piece_number, top_right):  # If top left is enemy
                    if board[tempi - 2][tempj + 2] == 0:
                        Leaper_can_capture += 1
                        break
                    else:
                        tempi -= 1
                        tempj += 1
                else:  # If top left is an ally
                    break
    if i != 7:
        tempi = i
        while tempi < 6:  # Checking below
            below = board[tempi + 1][j]
            if below == 0:  # If above is empty
                tempi += 1
                if kingi != -1 and tempi != kingi and j != kingj:
                    Coordinator_space += 1
            elif isEnemy(piece_number, below):  # If above is enemy
                if board[tempi + 2][j] == 0:  # enemy is capturable
                    Leaper_can_capture += 1
                    break
                else:
                    tempi += 1
            else:  # If above is an ally
                break
        if j != 0:  # if piece is not left
            tempj = j
            tempi = i
            while tempi < 6 and tempj > 2:  # Checking bottom left
                bottom_left = board[tempi + 1][tempj - 1]
                if bottom_left == 0:  # If bottom left is empty
                    tempi += 1
                    tempj -= 1
                    if kingi != -1 and tempi != kingi and tempj != kingj:
                        Coordinator_space += 1
                elif isEnemy(piece_number, bottom_left):  # If bottom left is enemy
                    if board[tempi + 2][tempj - 2] == 0:
                        Leaper_can_capture += 1
                        break
                    else:
                        tempi += 1
                        tempj -= 1
                else:  # If bottom left is an ally
                    break
        if j != 7:  # if piece is not left
            tempj = j
            tempi = i
            while tempi < 6 and tempj < 6:  # Checking bottom right
                bottom_right = board[tempi + 1][tempj + 1]
                if bottom_right == 0:  # If bottom right is empty
                    tempi += 1
                    tempj += 1
                    if kingi != -1 and tempi != kingi and tempj != kingj:
                        Coordinator_space += 1
                elif isEnemy(piece_number, bottom_right):  # If bottom right is enemy
                    if board[tempi + 2][tempj + 2] == 0:
                        Leaper_can_capture += 1
                        break
                    else:
                        tempi += 1
                        tempj += 1
                else:  # If bottom right is an ally
                    break
    if j != 0:
        tempj = j
        while tempj > 2:  # Checking left
            left = board[i][tempj - 1]
            if left == 0:  # If left is empty
                tempj -= 1
                if kingi != -1 and i != kingi and tempj != kingj:
                    Coordinator_space += 1
            elif isEnemy(piece_number, left):  # If left is enemy
                if board[i][tempj - 2] == 0:  # enemy is capturable
                    Leaper_can_capture += 1
                    break
                else:
                    tempj -= 1
            else:  # If right is an ally
                break
    if j != 7:
        tempj = j
        while tempj < 6:  # Checking right
            right = board[i][tempj + 1]
            if right == 0:  # If right is empty
                tempj += 1
                if kingi != -1 and i != kingi and tempj != kingj:
                    Coordinator_space += 1
            elif isEnemy(piece_number, right):  # If right is enemy
                if board[i][tempj + 2] == 0:  # enemy is capturable
                    Leaper_can_capture += 1
                    break
                else:
                    tempj += 1
            else:  # If right is ally
                break
    which_piece = piece_number // 2
    if which_piece == 2:  # If the piece is coordinator
        return Coordinator_space
    return Leaper_can_capture


#  Takes in the coordinates of the piece, current board, and boolean
#  Calculates the number of nearby pieces
#  When the which_piece is an Imitator, it calculates the values of surrounding pieces
#  Returns the number, Returns the surrounding value if Imitator
def surrounding_pieces(i, j, board, which_piece, piece_number):
    surroundings = 0
    Next_to_imitator = 0  # Value of the surrounding enemy pieces
    if i != 0:  # If piece is not top side
        if isEnemy(piece_number, board[i - 1][j]):  # Check above
            surroundings += 1
            if which_piece == 4:  # If the piece is Imitator
                Next_to_imitator -= PIECE_EVALUATION[board[i - 1][j]]
        if which_piece != 1:  # If it isn't a pincer
            if j != 0:  # If piece is not left
                if isEnemy(piece_number, board[i - 1][j - 1]):  # check top-left
                    surroundings += 1
                    if which_piece == 4:
                        Next_to_imitator -= PIECE_EVALUATION[board[i - 1][j]]
            if j != 7:  # If piece is not right
                if isEnemy(piece_number, board[i - 1][j + 1]):  # check top-right
                    surroundings += 1
                    if which_piece == 4:
                        Next_to_imitator -= PIECE_EVALUATION[board[i - 1][j + 1]]
    if i != 7:  # If piece is not bottom side
        if isEnemy(piece_number, board[i + 1][j]):  # Check below
            surroundings += 1
            if which_piece == 4:
                Next_to_imitator -= PIECE_EVALUATION[board[i + 1][j]]
        if which_piece != 1:  # If it isn't a pincer
            if j != 0:  # If piece is not left
                if isEnemy(piece_number, board[i + 1][j - 1]):  # check bottom-left
                    surroundings += 1
                    if which_piece == 4:
                        Next_to_imitator -= PIECE_EVALUATION[board[i + 1][j - 1]]
            if j != 7:  # If piece is not right
                if isEnemy(piece_number, board[i + 1][j + 1]):  # check bottom-right
                    surroundings += 1
                    if which_piece == 4:
                        Next_to_imitator -= PIECE_EVALUATION[board[i + 1][j + 1]]
    if j != 0:  # If piece is not left side
        if isEnemy(piece_number, board[i][j - 1]):  # Check left
            surroundings += 1
            if which_piece == 4:
                Next_to_imitator -= PIECE_EVALUATION[board[i][j - 1]]
    if j != 7:  # If piece is not right side
        if isEnemy(piece_number, board[i][j + 1]):  # Check right
            surroundings += 1
            if which_piece == 4:
                Next_to_imitator -= PIECE_EVALUATION[board[i][j + 1]]
    if which_piece == 4:
        return Next_to_imitator
    return surroundings


# Takes in the number of the current piece, and the piece to check
# Returns whether that piece to check is an enemy or not
def isEnemy(piece, enemy):
    if enemy == 0:
        return False
    color = piece % 2
    if enemy % 2 == color:
        return False
    return True


KING_BOARD_EARLY = [-40, -50, -50, -50, -50, -50, -50, -40,
                    -40, -40, -40, -40, -40, -40, -40, -40,
                    -30, -30, -30, -30, -30, -30, -30, -30,
                    -30, -30, -30, -30, -30, -30, -30, -30,
                    -20, -20, -20, -10, -10, -20, -20, -20,
                    -10, -10, -10, -5, -5, -10, -10, -10,
                    0, 10, 5, 0, 0, 5, 10, 0,
                    10, 15, 10, 0, 0, 10, 15, 10]

# When more than 16 pieces are gone
KING_BOARD_LATE = [-30, -40, -30, -20, -20, -30, -40, -30,
                   -20, -30, -20, 5, 5, -20, -30, -20,
                   -10, -20, 5, 10, 10, 5, -20, -10,
                   -10, 5, 10, 20, 20, 10, 5, -10,
                   -10, 5, 10, 20, 20, 10, 5, -10,
                   -10, -20, 5, 10, 10, 5, -20, -10,
                   -20, -30, -20, 5, 5, -20, -30, -20,
                   -30, -40, -30, -20, -20, -30, -40, -30]

# Edges of the board are very safe
# Significant pressure on the enemy side
PINCER_BOARD = [20, 15, 15, 15, 15, 15, 15, 20,
                15, 5, 5, 5, 5, 5, 5, 15,
                12, 10, 10, 10, 10, 10, 10, 12,
                9, 5, -5, -10, -10, -5, 5, 9,
                6, 5, 0, 0, 0, 0, 5, 6,
                3, 5, 5, 5, 5, 5, 5, 3,
                0, 0, 0, 0, 0, 0, 0, 0,
                0, -5, -5, -5, -5, -5, -5, 0]

'''PINCER_BOARD = [-1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000,
                -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000,
                -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000,
                -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000,
                -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000,
                -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000,
                -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000,
                -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000
                ]'''

# Edges of the board makes Withdrawer limited
WITHDRAWER_BOARD = [-50, -40, -40, -40, -40, -40, -40, -50,
                    -40, -10, 0, 5, 5, 0, -10, -40,
                    -30, -5, 10, 20, 20, 10, -5, -30,
                    -20, 5, 20, 25, 25, 20, 5, -20,
                    -20, 5, 20, 25, 25, 20, 5, -20,
                    -30, -5, 10, 20, 20, 10, -5, -30,
                    -40, -10, 0, 5, 5, 0, -10, -40,
                    -50, -40, -40, -40, -40, -40, -40, -50]

# Similar to Pincer, edges keep leapers safe while allowing them to look for opportunities
LEAPER_BOARD = [40, 30, 20, 10, 10, 20, 30, 40,
                30, 15, 0, -5, -5, 0, 15, 30,
                20, 10, -5, -10, -10, -5, 10, 20,
                10, -5, -15, -25, -25, -15, -5, 10,
                10, -5, -15, -25, -25, -15, -5, 10,
                10, 0, -15, -20, -20, -20, 0, 10,
                20, 5, -10, -15, -15, -10, 5, 20,
                30, 20, 10, 0, 0, 10, 20, 30]

# Values of each pieces according to the INIT_TO_CODE
# Example: A white Pincer(P) is defined as 3 by INIT_TO_CODE, so third index of the array indicates the pincer's score
PIECE_EVALUATION = [0, 0, -100, 100, -800, 800, -700, 700, -1000, 1000, -600, 600, -50000, 50000, -900, 900]


def make_a_move(current_board, initial_position, final_position):
    board = [r[:] for r in current_board]
    initial_row = initial_position[0]
    initial_column = initial_position[1]
    final_row = final_position[0]
    final_column = final_position[1]
    piece = board[initial_row][initial_column]
    if piece == 2 or piece == 3:  # pincer
        return pincer_move_capture(board, [initial_row, initial_column], [final_row, final_column])
    elif piece == 4 or piece == 5:  # coordinator
        return coordinator_move_capture(board, [initial_row, initial_column], [final_row, final_column])
    elif piece == 6 or piece == 7:  # leaper
        return leaper_move_capture(board, [initial_row, initial_column], [final_row, final_column])
    elif piece == 8 or piece == 9:  # imitator
        return imitator_move_capture(board, [initial_row, initial_column], [final_row, final_column])
    elif piece == 10 or piece == 11:  # withdrawer
        return withdrawer_move_capture(board, [initial_row, initial_column], [final_row, final_column])
    elif piece == 12 or piece == 13:  # king
        return king_move_capture(board, [initial_row, initial_column], [final_row, final_column])
    elif piece == 14 or piece == 15:  # freezer
        return freezer_move(board, [initial_row, initial_column], [final_row, final_column])
    else:
        raise ValueError('This move is not legal')


def imitator_move_capture(current_board, initial_position, final_position):
    board = [r[:] for r in current_board]
    initial_row = inital_position[0]
    initial_column = initial_position[1]
    imitator = board[initial_row][initial_column]
    if not can_imitator_capture_coordinator(board, initial_position, final_position) and not \
            can_imitator_capture_king(board, initial_position) and not \
            can_imitator_capture_leaper(board, initial_position, final_position) and not \
            can_imitator_capture_pincer(board, initial_position, final_position) and not \
            can_imitator_capture_withdrawer(board, initial_position, final_position):
        if not can_queen_move(board, initial_position, final_position):
            raise ValueError('This move is not legal')
        board[final_row][final_column] = imitator
        board[initial_row][initial_column] = 0
        return board
    if can_imitator_capture_king(board, initial_position):
        return king_capture(board, initial_position, final_position)
    elif can_imitator_capture_leaper(board, initial_position, final_position):
        return leaper_move_capture(board, initial_position, final_position)
    elif can_imitator_capture_coordinator(board, initial_position, final_position):
        return coordinator_capture(board, final_position)
    elif can_imitator_capture_withdrawer(board, initial_position, final_position):
        return withdrawer_move_capture(board, initial_position, final_position)
    elif can_imitator_capture_pincer(board, initial_position, final_position):
        return imitator_move_capture(board, initial_position, final_position)
    return board


def can_imitator_capture_king(current_board, imitator_position):
    board = [r[:] for r in current_board]
    initial_row = imitator_position[0]
    initial_column = imitator_position[1]
    imitator = board[initial_row][initial_column]
    if is_adjacent_to_enemy_freezer(board, [initial_row, initial_column]):
        return False
    king = 13  # white king
    if imitator % 2 == 1:
        king = 12  # black king
    r1 = initial_row - 1
    r2 = initial_row + 1
    c1 = initial_column - 1
    c2 = initial_column + 1
    if r1 >= 0 and board[r1][initial_column] == king:
        return True
    elif r2 <= 7 and board[r2][initial_column] == king:
        return True
    elif c1 >= 0 and board[initial_row][c1] == king:
        return True
    elif c2 <= 7 and board[initial_row][c2] == king:
        return True
    elif r1 >= 0 and c1 >= 0 and board[r1][c1] == king:
        return True
    elif r2 <= 7 and c1 >= 0 and board[r2][c1] == king:
        return True
    elif r1 >= 0 and c2 <= 7 and board[r1][c2] == king:
        return True
    elif r2 <= 7 and c2 <= 7 and board[r2][c2] == king:
        return True
    return False


def can_imitator_capture_withdrawer(current_board, initial_position, final_position):
    board = [r[:] for r in current_board]
    initial_row = initial_position[0]
    initial_column = initial_position[1]
    imitator = board[initial_row][initial_column]
    withdrawer = 11  # white withdrawer
    if imitator % 2 == 1:
        withdrawer = 10  # black withdrawer
    r1 = initial_row - 1
    r2 = initial_row + 1
    c1 = initial_column - 1
    c2 = initial_column + 1
    if r1 >= 0 and board[r1][initial_column] == withdrawer:
        try:
            withdrawer_move_capture(current_board, initial_position, final_position)
            return True
        except ValueError:
            return False
    elif r2 <= 7 and board[r2][initial_column] == withdrawer:
        try:
            withdrawer_move_capture(current_board, initial_position, final_position)
            return True
        except ValueError:
            return False
    elif c1 >= 0 and board[initial_row][c1] == withdrawer:
        try:
            withdrawer_move_capture(current_board, initial_position, final_position)
            return True
        except ValueError:
            return False
    elif c2 <= 7 and board[initial_row][c2] == withdrawer:
        try:
            withdrawer_move_capture(current_board, initial_position, final_position)
            return True
        except ValueError:
            return False
    elif r1 >= 0 and c1 >= 0 and board[r1][c1] == withdrawer:
        try:
            withdrawer_move_capture(current_board, initial_position, final_position)
            return True
        except ValueError:
            return False
    elif r2 <= 7 and c1 >= 0 and board[r2][c1] == withdrawer:
        try:
            withdrawer_move_capture(current_board, initial_position, final_position)
            return True
        except ValueError:
            return False
    elif r1 >= 0 and c2 <= 7 and board[r1][c2] == withdrawer:
        try:
            withdrawer_move_capture(current_board, initial_position, final_position)
            return True
        except ValueError:
            return False
    elif r2 <= 7 and c2 <= 7 and board[r2][c2] == withdrawer:
        try:
            withdrawer_move_capture(current_board, initial_position, final_position)
            return True
        except ValueError:
            return False


def can_imitator_capture_pincer(current_board, initial_position, final_position):
    if not can_pincer_move(current_board, initial_position, final_position):
        return False
    board = [r[:] for r in current_board]
    row = final_position[0]
    column = final_position[1]
    imitator = board[row][column]
    pincer = 3  # white pincer
    if imitator % 2 == 1:
        pincer = 2  # black pincer
    r1 = row - 2
    r2 = row + 2
    c1 = column - 2
    c2 = column + 2
    if r1 >= 0 and board[row - 1][column] == pincer and isFriendly(imitator, board[r1][column]):
        return True
    elif r2 <= 7 and board[row + 1][column] == pincer and isFriendly(imitator, board[r2][column]):
        return True
    elif c1 >= 0 and board[row][column - 1] == pincer and isFriendly(imitator, board[row][c1]):
        return True
    elif c2 <= 7 and board[row][column + 1] == pincer and isFriendly(imitator, board[row][c2]):
        return True
    return False


def can_imitator_capture_coordinator(current_board, initial_position, final_position):
    if not can_queen_move(current_board, initial_position, final_position):
        return False
    board = [r[:] for r in current_board]
    coord_row = final_position[0]
    coord_column = final_position[1]
    imitator = board[coord_row][coord_column]
    coordinator = 5  # white coordinator
    if imitator % 2 == 1:
        coordinator = 4  # black coordinator
    king_row = 0
    king_column = 0
    if imitator == 9:  # looking for white king
        for r in range(8):
            for c in range(8):
                if board[r][c] == 13:
                    king_row = r
                    king_column = c
                    break
                else:
                    continue
            break
    elif imitator == 8:  # looking for black king
        for r in range(8):
            for c in range(8):
                if board[r][c] == 12:
                    king_row = r
                    king_column = c
                    break
                else:
                    continue
            break
    if board[king_row][coord_column] == coordinator or board[coord_row][king_column] == coordinator:
        return True
    return False


def can_imitator_capture_leaper(current_board, initial_position, final_position):
    if not can_leaper_capture(current_board, initial_position, final_position):
        return False
    board = [r[:] for r in current_board]
    initial_row = initial_position[0]
    initial_column = initial_position[1]
    final_row = final_position[0]
    final_column = final_position[1]
    imitator = board[initial_row][initial_column]
    if is_adjacent_to_enemy_freezer(board, [initial_row, initial_column]):
        return False
    leaper = 7  # white leaper
    if imitator % 2 == 1:
        leaper = 6  # black leaper
    row_diff = abs(final_row - initial_row)
    column_diff = abs(final_column - initial_column)
    if final_row < initial_row and final_column == initial_column:
        if board[final_row + 1][initial_column] == leaper:
            return True
        return False
    elif final_row > initial_row and final_column == initial_column:
        if board[final_row - 1][initial_column] == leaper:
            return True
        return False
    elif final_column < initial_column and final_row == initial_row:
        if board[initial_row][final_column + 1] == leaper:
            return True
        return False
    elif final_column > initial_column and final_row == initial_row:
        if board[initial_row][final_column - 1] == leaper:
            return True
        return False
    if final_row > initial_row and final_column > initial_column and row_diff == column_diff:
        if board[final_row - 1][final_column - 1] == leaper:
            return True
        return False
    elif final_row > initial_row and final_column < initial_column and row_diff == column_diff:
        if board[final_row - 1][final_column + 1] == leaper:
            return True
        return False
    elif final_row < initial_row and final_column > initial_column and row_diff == column_diff:
        if board[final_row + 1][final_column - 1] == leaper:
            return True
        return False
    elif final_row < initial_row and final_column < initial_column and row_diff == column_diff:
        if board[final_row + 1][final_column + 1] == leaper:
            return True
        return False
    return False


def king_move_capture(current_board, initial_position, final_position):
    board = [r[:] for r in current_board]
    initial_row = initial_position[0]
    initial_column = initial_position[1]
    final_row = final_position[0]
    final_column = final_position[1]
    if not can_king_move(board, [initial_row, initial_column], [final_row, final_column]):
        raise ValueError('This move is not legal')
    return king_capture(board, [initial_row, initial_column], [final_row, final_column])


def can_king_move(current_board, initial_position, final_position):
    board = [r[:] for r in current_board]
    initial_row = initial_position[0]
    initial_column = initial_position[1]
    final_row = final_position[0]
    final_column = final_position[1]
    if initial_row == final_row and initial_column == final_column:
        return False
    if final_row < 0 or final_row > 7 or final_column < 0 or final_column > 7:
        return False
    if is_adjacent_to_enemy_freezer(board, [initial_row, initial_column]):
        return False
    if abs(final_row - initial_row) < 2 and abs(final_column - initial_column) < 2:
        if board[final_row][final_column] == 0:
            return True
    return False


def king_capture(current_board, initial_position, final_position):
    board = [r[:] for r in current_board]
    initial_row = initial_position[0]
    initial_column = initial_position[1]
    final_row = final_position[0]
    final_column = final_position[1]
    king = board[initial_row][initial_column]
    if abs(final_row - initial_row) < 2 and abs(final_column - initial_column) < 2 and isEnemy(king, board[final_row][
        final_column]):
        board[final_row][final_column] = king
        board[initial_row][initial_column] = 0
    return board


def pincer_move_capture(current_board, initial_position, final_position):
    board = [r[:] for r in current_board]
    initial_row = initial_position[0]
    initial_column = initial_position[1]
    final_row = final_position[0]
    final_column = final_position[1]
    pincer = board[initial_row][initial_column]
    if not can_pincer_move(board, [initial_row, initial_column], [final_row, final_column]):
        raise ValueError('This move is not legal')
    board[final_row][final_column] = pincer
    board[initial_row][initial_column] = 0
    return pincer_capture(board, [final_row, final_column])


def can_pincer_move(current_board, initial_position, final_position):
    board = [r[:] for r in current_board]
    initial_row = initial_position[0]
    initial_column = initial_position[1]
    final_row = final_position[0]
    final_column = final_position[1]
    if initial_row == final_row and initial_column == final_column:
        return False
    if final_row < 0 or final_row > 7 or final_column < 0 or final_column > 7:
        return False
    if board[final_row][final_column] is not 0:
        return False
    if is_adjacent_to_enemy_freezer(board, [initial_row, initial_column]):
        return False
    if final_row > initial_row and final_column == initial_column:  # movement vertically down
        for r in range(initial_row + 1, final_row):
            if board[r][final_column] is not 0:
                return False
        return True
    elif final_row < initial_row and final_column == initial_column:  # movement vertically up
        for r in range(initial_row - 1, final_row, -1):
            if board[r][final_column] is not 0:
                return False
        return True
    elif final_column > initial_column and initial_row == final_row:  # movement horizontally right
        for c in range(initial_column + 1, final_column):
            if board[final_row][c] is not 0:
                return False
        return True
    elif final_column < initial_column and initial_row == final_row:  # movement horizontally left
        for c in range(initial_column - 1, final_column, -1):
            if board[final_row][c] is not 0:
                return False
        return True
    return False


def can_queen_move(current_board, initial_position, final_position):
    board = [r[:] for r in current_board]
    initial_row = initial_position[0]
    initial_column = initial_position[1]
    final_row = final_position[0]
    final_column = final_position[1]
    if initial_row == final_row and initial_column == final_column:
        return False
    if final_row < 0 or final_row > 7 or final_column < 0 or final_column > 7:
        return False
    if board[final_row][final_column] is not 0:
        return False
    if is_adjacent_to_enemy_freezer(board, [initial_row, initial_column]):
        return False
    row_diff = abs(final_row - initial_row)
    column_diff = abs(final_column - initial_column)
    if final_row > initial_row and final_column == initial_column:  # movement vertically down
        for r in range(initial_row + 1, final_row):
            if board[r][final_column] is not 0:
                return False
        return True
    elif final_row < initial_row and final_column == initial_column:  # movement vertically up
        for r in range(initial_row - 1, final_row, -1):
            if board[r][final_column] is not 0:
                return False
        return True
    elif final_column > initial_column and initial_row == final_row:  # movement horizontally right
        for c in range(initial_column + 1, final_column):
            if board[final_row][c] is not 0:
                return False
        return True
    elif final_column < initial_column and initial_row == final_row:  # movement horizontally left
        for c in range(initial_column - 1, final_column, -1):
            if board[final_row][c] is not 0:
                return False
        return True
    elif final_row > initial_row and final_column > initial_column and row_diff == column_diff:  # movement diagonally down and to the right
        r = initial_row + 1
        c = initial_column + 1
        while r is not final_row and c is not final_column:
            if board[r][c] is not 0:
                return False
            r += 1
            c += 1
        return True
    elif final_row < initial_row and final_column > initial_column and row_diff == column_diff:  # movement diagonally up and to the right
        r = initial_row - 1
        c = initial_column + 1
        while r is not final_row and c is not final_column:
            if board[r][c] is not 0:
                return False
            r -= 1
            c += 1
        return True
    elif final_row > initial_row and final_column < initial_column and row_diff == column_diff:  # movement diagonally down and to the left
        r = initial_row + 1
        c = initial_column - 1
        while r is not final_row and c is not final_column:
            if board[r][c] is not 0:
                return False
            r += 1
            c -= 1
        return True
    elif final_row < initial_row and final_column < initial_column and row_diff == column_diff:  # movement diagonally up and to the left
        r = initial_row - 1
        c = initial_column - 1
        while r is not final_row and c is not final_column:
            if board[r][c] is not 0:
                return False
            r -= 1
            c -= 1
        return True
    return False


def freezer_move(current_board, initial_position, final_position):
    board = [r[:] for r in current_board]
    initial_row = initial_position[0]
    initial_column = initial_position[1]
    final_row = final_position[0]
    final_column = final_position[1]
    freezer = board[initial_row][initial_column]
    if not can_queen_move(board, [initial_row, initial_column], [final_row, final_column]):
        raise ValueError('This move is not legal')
    board[final_row][final_column] = freezer
    board[initial_row][initial_column] = 0
    return board


# queen = any piece that moves like a queen in chess
def coordinator_move_capture(current_board, initial_position, final_position):
    board = [r[:] for r in current_board]
    initial_row = initial_position[0]
    initial_column = initial_position[1]
    final_row = final_position[0]
    final_column = final_position[1]
    queen = board[initial_row][initial_column]
    if not can_queen_move(board, [initial_row, initial_column], [final_row, final_column]):
        raise ValueError('This move is not legal')
    board[final_row][final_column] = queen
    board[initial_row][initial_column] = 0
    return coordinator_capture(board, [final_row, final_column])


def pincer_capture(current_board, position):
    board = [r[:] for r in current_board]
    row = position[0]
    column = position[1]
    pincer = board[row][column]
    r1 = row - 2
    r2 = row + 2
    c1 = column - 2
    c2 = column + 2
    if r1 >= 0 and isEnemy(pincer, board[row - 1][column]) and isFriendly(pincer, board[r1][column]):
        board[row - 1][column] = 0
    if r2 <= 7 and isEnemy(pincer, board[row + 1][column]) and isFriendly(pincer, board[r2][column]):
        board[row + 1][column] = 0
    if c1 >= 0 and isEnemy(pincer, board[row][column - 1]) and isFriendly(pincer, board[row][c1]):
        board[row][column - 1] = 0
    if c2 <= 7 and isEnemy(pincer, board[row][column + 1]) and isFriendly(pincer, board[row][c2]):
        board[row][column + 1] = 0
    return board


def coordinator_capture(current_board, position):
    board = [r[:] for r in current_board]
    coord_row = position[0]
    coord_column = position[1]
    coordinator = board[coord_row][coord_column]
    king_row = 0
    king_column = 0
    coordinate = findKing(board, coordinator)
    king_row = coordinate[0]
    king_column = coordinate[1]
    # if coordinator == 6:  # looking for white king
    #     for r in range(8):
    #         for c in range(8):
    #             if board[r][c] == 13:
    #                 king_row = r
    #                 king_column = c
    #                 break
    #             else:
    #                 continue
    #         break
    # elif coordinator == 5:  # looking for black king
    #     for r in range(8):
    #         for c in range(8):
    #             if board[r][c] == 12:
    #                 king_row = r
    #                 king_column = c
    #                 break
    #             else:
    #                 continue
    #         break
    if not isFriendly(board[king_row][coord_column], coordinator):
        board[king_row][coord_column] = 0
    if not isFriendly(board[coord_row][king_column], coordinator):
        board[coord_row][king_column] = 0
    return board


def withdrawer_move_capture(current_board, initial_position, final_position):
    board = [r[:] for r in current_board]
    initial_row = initial_position[0]
    initial_column = initial_position[1]
    final_row = final_position[0]
    final_column = final_position[1]
    if not can_queen_move(board, [initial_row, initial_column], [final_row, final_column]):
        raise ValueError('This move is not legal')
    withdrawer = board[initial_row][initial_column]
    row_diff = abs(final_row - initial_row)
    column_diff = abs(final_column - initial_column)
    if final_row > initial_row and final_column == initial_column and initial_row > 0:  # movement vertically down
        if isEnemy(withdrawer, board[initial_row - 1][initial_column]):
            board[initial_row - 1][initial_column] = 0
    elif final_row < initial_row and final_column == initial_column and initial_row < 7:  # movement vertically up
        if isEnemy(withdrawer, board[initial_row + 1][initial_column]):
            board[initial_row + 1][initial_column] = 0
    elif final_column > initial_column and initial_row == final_row and initial_column > 0:  # movement horizontally right
        if isEnemy(withdrawer, board[initial_row][initial_column - 1]):
            board[initial_row][initial_column - 1] = 0
    elif final_column < initial_column and initial_row == final_row and initial_column < 7:  # movement horizontally left
        if isEnemy(withdrawer, board[initial_row][initial_column + 1]):
            board[initial_row][initial_column + 1] = 0
    elif final_row > initial_row and final_column > initial_column and row_diff == column_diff and initial_row > 0 and initial_column > 0:  # movement diagonally down and to the right
        if isEnemy(withdrawer, board[initial_row - 1][initial_column - 1]):
            board[initial_row - 1][initial_column - 1] = 0
    elif final_row < initial_row and final_column > initial_column and row_diff == column_diff and initial_row < 7 and initial_column > 0:  # movement diagonally up and to the right
        if isEnemy(withdrawer, board[initial_row + 1][initial_column - 1]):
            board[initial_row + 1][initial_column - 1] = 0
    elif final_row > initial_row and final_column < initial_column and row_diff == column_diff and initial_row > 0 and initial_column < 7 :  # movement diagonally down and to the left
        if isEnemy(withdrawer, board[initial_row - 1][initial_column + 1]):
            board[initial_row - 1][initial_column + 1] = 0
    elif final_row < initial_row and final_column < initial_column and row_diff == column_diff and initial_row < 7 and initial_column < 7:  # movement diagonally up and to the left
        if isEnemy(withdrawer, board[initial_row + 1][initial_column + 1]):
            board[initial_row + 1][initial_column + 1] = 0
    board[final_row][final_column] = withdrawer
    board[initial_row][initial_column] = 0
    return board


def can_leaper_capture(current_board, initial_position, final_position):
    board = [r[:] for r in current_board]
    initial_row = initial_position[0]
    initial_column = initial_position[1]
    final_row = final_position[0]
    final_column = final_position[1]
    if board[final_row][final_column] is not 0:
        return False
    if is_adjacent_to_enemy_freezer(board, [initial_row, initial_column]):
        return False
    leaper = board[initial_row][initial_column]
    row_diff = abs(final_row - initial_row)
    column_diff = abs(final_column - initial_column)
    if final_row < initial_row and final_column == initial_column:
        for r in range(initial_row - 1, final_row + 1, -1):
            if board[r][initial_column] is not 0:
                return False
        if isEnemy(leaper, board[final_row + 1][initial_column]) and abs(final_row + 1 - initial_row) > 1:
            return True
        return False
    elif final_row > initial_row and final_column == initial_column:
        for r in range(initial_row + 1, final_row - 1):
            if board[r][initial_column] is not 0:
                return False
        if isEnemy(leaper, board[final_row - 1][initial_column]) and abs(final_row - 1 - initial_row) > 1:
            return True
        return False
    elif final_column < initial_column and final_row == initial_row:
        for c in range(initial_column - 1, final_column + 1, -1):
            if board[initial_row][c] is not 0:
                return False
        if isEnemy(leaper, board[initial_row][final_column + 1]) and abs(final_column + 1 - initial_column) > 1:
            return True
        return False
    elif final_column > initial_column and final_row == initial_row:
        for c in range(initial_column + 1, final_column - 1):
            if board[initial_row][c] is not 0:
                return False
        if isEnemy(leaper, board[initial_row][final_column - 1]) and abs(final_column - 1 - initial_column) > 1:
            return True
        return False
    if final_row > initial_row and final_column > initial_column and row_diff == column_diff:
        r = initial_row + 1
        c = initial_column + 1
        while r is not final_row - 1 and c is not final_column - 1:
            if board[r][c] is not 0:
                return False
            r += 1
            c += 1
        if isEnemy(leaper, board[final_row - 1][final_column - 1]) and abs(final_row - 1 - initial_row) > 1 and abs(
                                final_column - 1 - initial_column) > 1:
            return True
        return False
    elif final_row > initial_row and final_column < initial_column and row_diff == column_diff:
        r = initial_row + 1
        c = initial_column - 1
        while r is not final_row - 1 and c is not final_column + 1:
            if board[r][c] is not 0:
                return False
            r += 1
            c -= 1
        if isEnemy(leaper, board[final_row - 1][final_column + 1]) and abs(final_row - 1 - initial_row) > 1 and abs(
                                final_column + 1 - initial_column) > 1:
            return True
        return False
    elif final_row < initial_row and final_column > initial_column and row_diff == column_diff:
        r = initial_row - 1
        c = initial_column + 1
        while r is not final_row + 1 and c is not final_column - 1:
            if board[r][c] is not 0:
                return False
            r -= 1
            c += 1
        if isEnemy(leaper, board[final_row + 1][final_column - 1]) and abs(final_row + 1 - initial_row) > 1 and abs(
                                final_column - 1 - initial_column) > 1:
            return True
        return False
    elif final_row < initial_row and final_column < initial_column and row_diff == column_diff:
        r = initial_row - 1
        c = initial_column - 1
        while r is not final_row + 1 and c is not final_column + 1:
            if board[r][c] is not 0:
                return False
            r -= 1
            c -= 1
        if isEnemy(leaper, board[final_row + 1][final_column + 1]) and abs(final_row + 1 - initial_row) > 1 and abs(
                                final_column + 1 - initial_column) > 1:
            return True
        return False
    return False


# BIG ASSUMPTION: ONCE WE ARE GIVEN A MOVE THAT CAPTURES A PIECE, WE TAKE THAT PIECE BY DEFAULT
# (i.e., it is not possible for us to move to make a move that captures a piece and not
# remove that piece from the board
def leaper_move_capture(current_board, initial_position, final_position):
    board = [r[:] for r in current_board]
    initial_row = initial_position[0]
    initial_column = initial_position[1]
    final_row = final_position[0]
    final_column = final_position[1]
    leaper = board[initial_row][initial_column]
    row_diff = abs(final_row - initial_row)
    column_diff = abs(final_column - initial_column)
    if not can_leaper_capture(board, [initial_row, initial_column], [final_row, final_column]):
        if not can_queen_move(board, [initial_row, initial_column], [final_row, final_column]):
            raise ValueError('This move is not legal')
        # just a regular move (no captures)
        board[final_row][final_column] = leaper
        board[initial_row][initial_column] = 0
        return board
    if final_row < initial_row and final_column == initial_column:
        board[final_row + 1][initial_column] = 0
    elif final_row > initial_row and final_column == initial_column:
        board[final_row - 1][initial_column] = 0
    elif final_column < initial_column and final_row == initial_row:
        board[initial_row][final_column + 1] = 0
    elif final_column > initial_column and final_row == initial_row:
        board[initial_row][final_column - 1] = 0
    elif final_row > initial_row and final_column > initial_column and row_diff == column_diff:
        board[final_row - 1][final_column - 1] = 0
    elif final_row > initial_row and final_column < initial_column and row_diff == column_diff:
        board[final_row - 1][final_column + 1] = 0
    elif final_row < initial_row and final_column > initial_column and row_diff == column_diff:
        board[final_row + 1][final_column - 1] = 0
    elif final_row < initial_row and final_column < initial_column and row_diff == column_diff:
        board[final_row + 1][final_column + 1] = 0
    board[final_row][final_column] = leaper
    board[initial_row][initial_column] = 0
    return board


def can_imitator_capture_king(current_board, imitator_position):
    board = [r[:] for r in current_board]
    initial_row = imitator_position[0]
    initial_column = imitator_position[1]
    imitator = board[initial_row][initial_column]
    if is_adjacent_to_enemy_freezer(board, [initial_row, initial_column]):
        return False
    king = 13  # white king
    if imitator % 2 == 1:
        king = 12  # black king
    r1 = initial_row - 1
    r2 = initial_row + 1
    c1 = initial_column - 1
    c2 = initial_column + 1
    if r1 >= 0 and board[r1][initial_column] == king:
        return True
    if r2 <= 7 and board[r2][initial_column] == king:
        return True
    if c1 >= 0 and board[initial_row][c1] == king:
        return True
    if c2 <= 7 and board[initial_row][c2] == king:
        return True
    if r1 >= 0 and c1 >= 0 and board[r1][c1] == king:
        return True
    if r2 <= 7 and c1 >= 0 and board[r2][c1] == king:
        return True
    if r1 >= 0 and c2 <= 7 and board[r1][c2] == king:
        return True
    if r2 <= 7 and c2 <= 7 and board[r2][c2] == king:
        return True
    return False


def is_adjacent_to_enemy_freezer(board, piece_position):
    row = piece_position[0]
    column = piece_position[1]
    freezer = 15  # white freezer
    if board[row][column] % 2 == 1:
        freezer = 14  # black freezer
    r1 = row - 1
    r2 = row + 1
    c1 = column - 1
    c2 = column + 1
    if r1 >= 0 and board[r1][column] == freezer:
        return True
    if r2 <= 7 and board[r2][column] == freezer:
        return True
    if c1 >= 0 and board[row][c1] == freezer:
        return True
    if c2 <= 7 and board[row][c2] == freezer:
        return True
    if r1 >= 0 and c1 >= 0 and board[r1][c1] == freezer:
        return True
    if r2 <= 7 and c1 >= 0 and board[r2][c1] == freezer:
        return True
    if r1 >= 0 and c2 <= 7 and board[r1][c2] == freezer:
        return True
    if r2 <= 7 and c2 <= 7 and board[r2][c2] == freezer:
        return True
    return False


def isFriendly(piece, friendly):
    if piece == 0 or friendly == 0:
        return False
    return piece % 2 == friendly % 2