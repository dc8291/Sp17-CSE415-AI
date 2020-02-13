'''Daniel Chai, CSE 415, May 30th 2017
33-Peg puzzle formulation'''

import copy

# <METADATA>
PROBLEM_NAME = "33-peg"
PROBLEM_AUTHORS = ['Daniel Chai']
PROBLEM_CREATION_DATE = "30-May-2017"
PROBLEM_DESC = \
    '''Formulation of 33-Peg Solitaire English version game.'''
# </METADATA>

REWARD = 1000
PENALTY = -400

Initial_state = [[0, 0, 1, 1, 1, 0, 0],
                 [0, 0, 1, 1, 1, 0, 0],
                 [1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 2, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1],
                 [0, 0, 1, 1, 1, 0, 0],
                 [0, 0, 1, 1, 1, 0, 0]]

def number_of_pegs(state):
    peg = 0
    for x in range(7):
        for y in range(7):
            if state.board[x][y] == 1:
                peg += 1
    return peg

def all_possible_moves(state):
    moves = []
    for n in OPERATORS:
        if n.is_applicable(state):
            moves.append(n)
    return moves

# <STATE>
class State():
    def __init__(self, board):
        self.board = board

    def __str__(self):
        # Produces a brief textual description of a state.
        s = ''
        for x in range(7):
            for y in range(7):
                s += str(self.board[x][y]) + " "
            s += "\n"
        s += "\n"
        return s

    def __eq__(self, s2):
        if not (type(self) == type(s2)):
            return False
        b1 = self.board
        b2 = s2.board
        for x in range(7):
            for y in range(7):
                if b1[x][y] != b2[x][y]:
                    return False
        return True

    def __hash__(self):
        return (str(self)).__hash__()

    def __copy__(self):
        # Performs an appropriately deep copy of a state,
        # for use by operators in creating new states.
        news = State([])
        board = [r[:] for r in self.board]
        news.board = board
        return news

# </STATE>

def can_move(s, position, movement):
    # 0 - represents illegal space
    # 1 - represents pegs
    # 2 - represents empty space
    x, y = position
    x_direction, y_direction = movement
    if s.board[x][y] != 1: return False
    if y_direction == 1:  # Moving up
        # If above is a peg and the space above is open
        if x < 2: return False
        if s.board[x - 2][y] == 0: return False
        if s.board[x - 1][y] == 1 and s.board[x - 2][y] == 2: return True
    if y_direction == -1:  # Moving down
        # If below is a peg and the space below is open
        if x > 4: return False
        if s.board[x + 2][y] == 0: return False
        if s.board[x + 1][y] == 1 and s.board[x + 2][y] == 2: return True
    if x_direction == -1:  # Moving right
        # If right is a peg and the space right is open
        if y > 4: return False
        if s.board[x][y + 2] == 0: return False
        if s.board[x][y + 1] == 1 and s.board[x][y + 2] == 2: return True
    if x_direction == 1:  # Moving left
        # If left is a peg and the space left is open
        if y < 2: return False
        if s.board[x][y - 2] == 0: return False
        if s.board[x][y - 1] == 1 and s.board[x][y - 2] == 2: return True
    return False # Default False



def move(s, position, movement):
    x, y = position
    x_direction, y_direction = movement
    temp_s = s.__copy__()
    temp_s.board[x][y] = 2  # Current location set to empty
    temp_s.board[x - y_direction][y - x_direction] = 2  # Peg in nearby set to empty
    temp_s.board[x - y_direction * 2][y - x_direction * 2] = 1  # Final location set to peg
    return temp_s


# <OPERATORS>
class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)


OPERATORS = []  # Contains all possible moves
for x in range(7):
    for y in range(7):
        for direction in ["up", "down", "left", "right"]:
            if direction == "up":
                x_direction = 0
                y_direction = 1
            if direction == "down":
                x_direction = 0
                y_direction = -1
            if direction == "left":
                x_direction = 1
                y_direction = 0
            if direction == "right":
                x_direction = -1
                y_direction = 0
            OPERATORS.append(Operator("Moving " + direction + " from (" + str(x) + ", " + str(y) + ")",
                                  lambda s, x1=x, y1=y, x2=x_direction, y2=y_direction: can_move(s, [x1,y1], [x2,y2]),
                                  lambda s, x1=x, y1=y, x2=x_direction, y2=y_direction: move(s, [x1,y1], [x2,y2])))
# </OPERATORS>


def T():
    return 1  # Deterministic


def R(s):
    if number_of_pegs(s) == 1:  # If there is only one peg on the board, that is goal state.
        return REWARD
    if not all_possible_moves(s):  # Find possible moves
        return PENALTY  # If list is empty
    return 0  # No penalty
