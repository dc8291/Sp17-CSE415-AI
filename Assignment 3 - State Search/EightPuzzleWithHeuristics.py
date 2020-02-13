''' Daniel Chai, CSE 415, April 18th 2017
    1532825'''

# <METADATA>

QUIET_VERSION = "0.2"
PROBLEM_NAME = "BasicEightPuzzle"
PROBLEM_VERSION = "0.2"
PROBLEM_AUTHORS = ['Daniel Chai']
PROBLEM_CREATION_DATE = "18-APR-2017"
PROBLEM_DESC = \
    '''This formulation of the Eight Puzzle uses generic
Python 3 constructs and has been tested with Python 3.6.'''


# </METADATA>

# <COMMON_CODE>

def can_move(s, From, To):
    '''Tests whether it's legal to move a piece in state s
     from the From location to the To location.'''
    try:
        pf = s.l[From]  # piece comes from
        pt = s.l[To]  # piece goes to
        if pf == 0: return False  # no piece to move.
        if pt == 0: return True  # no piece to worry about at destination.
        return False  # Piece at destination
    except (Exception) as e:
        print(e)


def move(s, From, To):
    '''Assuming it's legal to make the move, this computes
     the new state resulting from moving the piece from 
     From location to To destination.'''
    news = s.__copy__()  # start with a deep copy.
    l2 = news.l  # grab the new state's list.
    pf = l2[From]  # piece that will be moving
    l2[To] = pf  # move piece to To
    l2[From] = 0  # remove the piece from From
    return news  # return new state


def goal_test(s):
    '''If the list is same as Goal state, then it is goal state.'''
    return s.l == [0, 1, 2, 3, 4, 5, 6, 7, 8]


def goal_message(s):
    return "Put them in order!"


class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)


def h_euclidean(s):
    sum = 0
    for i in range(9):
        vertical = abs(s.l[i] // 3 - i // 3)
        horizontal = abs(s.l[i] % 3 - i % 3)
        sum += (vertical * vertical + horizontal * horizontal) ** 0.5
    return sum


def h_hamming(s):
    sum = 0
    for x in range(9):
        if s.l[x] != x:
            sum += 1
    return sum


def h_manhattan(s):
    sum = 0
    for i in range(9):
        vertical = abs(s.l[i] // 3 - i // 3)
        horizontal = abs(s.l[i] % 3 - i % 3)
        sum += vertical + horizontal
    return sum


def h_custom(s):
    sum = 0
    for x in range(9):
        sum += s.l[x] - x  # how far away the number is from
                           # where it is supposed to be on the array
    return sum + h_manhattan(s)


# </COMMON_CODE>

# <STATE>
class State():
    def __init__(self, l, f):
        self.l = l
        self.f = f

    def __str__(self):
        # Produces a brief textual description of a state.
        l = self.l
        return str(l)

    def __eq__(self, s2):
        if not (type(self) == type(s2)): return False
        l1 = self.l
        l2 = s2.l
        return l1 == l2

    def __hash__(self):
        return (str(self)).__hash__()

    def __copy__(self):
        # Performs an appropriately deep copy of a state,
        # for use by operators in creating new states.
        news = State([], 0)
        for x in self.l:
            news.l.append(x)
        return news

    def __lt__(self, other):
        return self.f < other.f


# </STATE>

# <OPERATORS>
combinations = [(0, 1), (0, 3), (1, 0), (1, 2), (1, 4), (2, 1), (2, 5), (3, 0), (3, 4), (3, 6),
                (4, 1), (4, 3), (4, 5), (4, 7), (5, 2), (5, 4), (5, 8), (6, 3), (6, 7), (7, 4),
                (7, 6), (7, 8), (8, 5), (8, 7)]
OPERATORS = [Operator("Moving piece " + str(p) + " to " + str(q),
                      lambda s, p1=p, q1=q: can_move(s, p1, q1),
                      # The default value construct is needed
                      # here to capture the values of p&q separately
                      # in each iteration of the list comp. iteration.
                      lambda s, p1=p, q1=q: move(s, p1, q1))
             for (p, q) in combinations]
# </OPERATORS>

# <INITIAL_STATE>
INITIAL_STATE = State([8, 7, 6, 5, 4, 3, 2, 1, 0], 0)
CREATE_INITIAL_STATE = lambda: INITIAL_STATE
# </INITIAL_STATE>

# <GOAL TEST>
GOAL_TEST = lambda s: goal_test(s)
CREATE_GOAL_STATE = lambda x: [0, 1, 2, 3, 4, 5, 6, 7, 8]
# </GOAL TEST>

# <GOAL_MESSAGE_FUNCTION>
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
# </GOAL_MESSAGE_FUNCTION>

# <HEURISTICS>
HEURISTICS = {'h_hamming': h_hamming, 'h_euclidean': h_euclidean, 'h_manhattan': h_manhattan, 'h_custom': h_custom}
# </HEURISTICS>
